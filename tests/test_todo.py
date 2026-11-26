import json
import tempfile
import unittest
from pathlib import Path

from todo import add_task, find_task, load_tasks, save_tasks


class TodoTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.data_file = Path(self.temp_dir.name) / "todos.json"

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_add_task_assigns_id_and_pending_status(self):
        tasks = []
        task = add_task(tasks, "Write tests")
        self.assertEqual(task["id"], 1)
        self.assertEqual(task["title"], "Write tests")
        self.assertFalse(task["completed"])

    def test_add_task_rejects_empty_title(self):
        with self.assertRaises(ValueError):
            add_task([], "   ")

    def test_save_and_load_round_trip(self):
        tasks = [add_task([], "First task")]
        save_tasks(tasks, self.data_file)
        self.assertEqual(load_tasks(self.data_file), tasks)

    def test_missing_file_returns_empty_list(self):
        self.assertEqual(load_tasks(self.data_file), [])

    def test_find_task_rejects_unknown_id(self):
        with self.assertRaises(ValueError):
            find_task([], 42)

    def test_invalid_json_is_reported(self):
        self.data_file.write_text("{invalid", encoding="utf-8")
        with self.assertRaises(RuntimeError):
            load_tasks(self.data_file)


if __name__ == "__main__":
    unittest.main()
