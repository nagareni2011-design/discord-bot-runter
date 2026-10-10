import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import database
import main


class ScreenshotTemplateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        patches = [
            patch.object(database, "DB_FILE", str(Path(self.temp.name) / "vending.json")),
            patch.object(database, "BACKUP_FILE", str(Path(self.temp.name) / "vending.json.bak")),
            patch.object(database, "LEGACY_DB_FILE", str(Path(self.temp.name) / "legacy.json")),
        ]
        for setting in patches:
            setting.start()
            self.addCleanup(setting.stop)

    def test_screenshot_machines_and_inventory_are_seeded(self):
        database.ensure_default_templates()

        expected = {
            "👑管理者販売👑": [1, 1],
            "✅管理者自販機販売✅": ["unlimited"],
            "payガチャ": [433, 185],
            "💎プロスピ石垢💎": [2, 10],
            "無料自販機": ["unlimited"],
            "ぷにぷにmod": ["unlimited"],
            "モンスト石垢": [5, 4, 3],
            "ドッカン石垢": [4],
            "💎レジェンズ石垢💎": [6, 6, 3],
            "イーフト石垢": [3, 5, 5, 5],
            "バウンティ石垢Android": [7, 4, 3, 5, 4, 8],
            "バウンティ石垢iOS": [0, 1, 3, 3, 3, 1],
        }
        for machine_name, stocks in expected.items():
            with self.subTest(machine=machine_name):
                items = database.get_items(machine_name)
                actual = [
                    "unlimited" if item["unlimited"] else len(item["contents"])
                    for item in items
                ]
                self.assertEqual(actual, stocks)
                for item in items:
                    self.assertTrue(
                        all(content == database.WARNING_CONTENT for content in item["contents"])
                    )

        self.assertNotIn("Gemini系", database.get_machine_names())
        self.assertNotIn("サブスクや便利系", database.get_machine_names())

    def test_catalog_refresh_runs_once_and_does_not_reset_sold_stock(self):
        database.ensure_default_templates()
        item = database.get_items("payガチャ")[0]
        database.update_item(item["id"], contents=item["contents"][:-1])

        self.assertEqual(database.ensure_default_templates(), 0)
        refreshed = database.get_item(item["id"])
        self.assertEqual(len(refreshed["contents"]), 432)

    def test_product_settings_selector_includes_all_restored_templates(self):
        view = main.ProductSettingsView()
        selector = view.children[0]

        self.assertEqual(
            {option.value for option in selector.options},
            {machine_name for machine_name, _ in database.DEFAULT_TEMPLATE_CATALOG},
        )

    def test_existing_panel_title_resolves_to_restored_machine_without_reposting(self):
        database.ensure_default_templates()
        with patch.object(main, "bot", SimpleNamespace(user=SimpleNamespace(id=42))):
            for machine_name in database.get_machine_names():
                if not database.get_items(machine_name):
                    continue
                with self.subTest(machine=machine_name):
                    interaction = SimpleNamespace(
                        channel_id=456,
                        message=SimpleNamespace(
                            id=789,
                            embeds=[SimpleNamespace(title=machine_name)],
                            author=SimpleNamespace(id=42),
                        ),
                    )
                    self.assertEqual(
                        main.resolve_panel_machine("old-name", interaction),
                        machine_name,
                    )

    def test_active_orders_defer_template_overwrite_until_safe(self):
        database.ensure_default_templates()
        item = database.get_items("payガチャ")[0]
        database.update_item(item["id"], contents=["temporary"])
        database.set_config(template_catalog_version=0)
        order = database.create_order(100, item["id"], 1)

        self.assertEqual(database.ensure_default_templates(), 0)
        self.assertEqual(database.get_item(item["id"])["contents"], ["temporary"])
        self.assertEqual(database.get_config("template_catalog_version"), 0)

        database.release_order(order["id"])
        database.ensure_default_templates()
        self.assertEqual(len(database.get_item(item["id"])["contents"]), 433)


if __name__ == "__main__":
    unittest.main()
