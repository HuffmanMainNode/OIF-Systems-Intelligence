import unittest
from oif_systems.inventory import validate_inventory, compare_snapshots
class Tests(unittest.TestCase):
 def test_diff(self):
  r=compare_snapshots({"software":[{"name":"a","version":"1"},{"name":"b","version":"1"}]},{"software":[{"name":"a","version":"2"},{"name":"c","version":"1"}]})
  self.assertEqual(r["added"],[{"name":"c","version":"1"}]); self.assertEqual(r["removed"],[{"name":"b","version":"1"}]); self.assertEqual(r["changed"],[{"name":"a","from":"1","to":"2"}])
 def test_invalid(self): self.assertTrue(validate_inventory({}))
 def test_duplicate(self):
  d={"host_id":"h","observed_at":"now","operating_system":{},"hardware":{},"software":[{"name":"A","version":"1"},{"name":"a","version":"2"}]}
  self.assertTrue(any("duplicate" in x for x in validate_inventory(d)))
if __name__ == "__main__": unittest.main()
