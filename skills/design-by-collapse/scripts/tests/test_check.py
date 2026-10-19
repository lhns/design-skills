import os
import subprocess
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
CHECK = os.path.join(HERE, "..", "check.py")


def run(name):
    p = subprocess.run([sys.executable, CHECK, os.path.join(HERE, name)],
                       capture_output=True, text=True, encoding="utf-8")
    return p.returncode, p.stdout


class CheckTest(unittest.TestCase):
    def test_clean(self):
        code, out = run("clean")
        self.assertEqual(code, 0, out)
        self.assertNotIn("ERRORS", out)
        self.assertNotIn("WARNINGS", out)
        self.assertIn("forks: 2 forced, 1 open, 0 conflict", out)

    def test_broken(self):
        code, out = run("broken")
        self.assertEqual(code, 1, out)
        expected = [
            "F1/a: W1 is a value; values only rank, they never eliminate",
            "F2/a: eliminated_by K50 does not exist",
            "F3/a: eliminated_by K3 is superseded/withdrawn",
            "F4/a: eliminated_by without why",
            "F5/b: preferred_by K1 is not an existing W id",
            "F6: conflict",
            "F7: forced to 'b' but chosen is 'z'",
            "F8: open fork missing question, default, decide_by",
            "F9: default 'c' is not a live option",
            "F10: chosen 'a' is eliminated; design shifted: move the choice",
            "no-trace: forced concept has no traces",
            "dead-trace: trace K3 is not a live K id",
            "floating-one: floating",
            "missing-fork: detail_of F99/a",
            "stranded-elim: stranded: re-attach or delete",
            "stranded-unchosen: stranded: re-attach or delete",
            "K4: from V99 not found in vision.md",
            "K2: duplicate id",
            "Q9: invalid id format",
            "K6: superseded_by 'K99'",
            "K7: superseded_by 'K3'",
            "round 2: concepts rose 3->7",
            "round 3: rules rose 3->4",
            "kernel changed since last count: recount",
            "K8: answers F11 but answer not propagated",
            "K9: answers F99 but answer not propagated",
        ]
        for msg in expected:
            self.assertIn(msg, out)
        self.assertEqual(out.count("[rule 3]"), 1)  # F10 reports rule 3 only, not rule 2
        self.assertNotIn("F10: forced", out)
        for n in range(1, 8):
            self.assertIn(f"[rule {n}]", out)
        self.assertIn("NEEDS OWNER", out)
        self.assertIn("WARNINGS", out)


if __name__ == "__main__":
    unittest.main()
