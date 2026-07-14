from django.core.management.base import BaseCommand
from telemetry.models import ScoringConfig
from telemetry.scoring import calculate_opi_score

class Command(BaseCommand):
    help = "Audits and verifies BKT & OPI estimation alignment with OSDE CCRA science blueprint performance cutoffs"

    def handle(self, *args, **options):
        self.stdout.write("==================================================")
        self.stdout.write("STARTING OSDE CCRA AUDIT & COMPLIANCE VERIFICATION")
        self.stdout.write("==================================================")

        # Get or create default scoring config
        config, created = ScoringConfig.objects.get_or_create(
            key="default",
            defaults={
                "a": 23.08,
                "b": 303.00,
                "advanced_cutoff": 327,
                "proficient_cutoff": 300,
                "basic_cutoff": 278
            }
        )

        self.stdout.write(f"Scoring Parameters: A={config.a}, B={config.b}")
        self.stdout.write(f"Cutoffs: Advanced={config.advanced_cutoff}, Proficient={config.proficient_cutoff}, Basic={config.basic_cutoff}")

        # Test Case 1: Baseline Student (85% accuracy, 3.0s response speed)
        # Expected theta = 0.0, OPI = 303 -> "Proficient"
        res_baseline = calculate_opi_score(85.0, 3.0)
        self.stdout.write(f"\n[TEST 1] Baseline Student: Accuracy=85.0%, Speed=3.0s")
        self.stdout.write(f"  -> OPI Score: {res_baseline['opi_score']} (Expected: 303)")
        self.stdout.write(f"  -> Band: {res_baseline['performance_band']} (Expected: Proficient)")
        assert res_baseline["opi_score"] == 303
        assert res_baseline["performance_band"] == "Proficient"
        self.stdout.write(self.style.SUCCESS("  - Baseline student alignment PASSED!"))

        # Test Case 2: Advanced Student (98% accuracy, 2.0s response speed)
        # Expected OPI >= 327 -> "Advanced"
        res_adv = calculate_opi_score(98.0, 2.0)
        self.stdout.write(f"\n[TEST 2] Advanced Student: Accuracy=98.0%, Speed=2.0s")
        self.stdout.write(f"  -> OPI Score: {res_adv['opi_score']}")
        self.stdout.write(f"  -> Band: {res_adv['performance_band']} (Expected: Advanced)")
        assert res_adv["opi_score"] >= config.advanced_cutoff
        assert res_adv["performance_band"] == "Advanced"
        self.stdout.write(self.style.SUCCESS("  - Advanced student alignment PASSED!"))

        # Test Case 3: Basic Student (80% accuracy, 3.0s response speed)
        # Expected OPI < 300 and >= 278 -> "Basic"
        res_basic = calculate_opi_score(80.0, 3.0)
        self.stdout.write(f"\n[TEST 3] Basic Student: Accuracy=80.0%, Speed=3.0s")
        self.stdout.write(f"  -> OPI Score: {res_basic['opi_score']}")
        self.stdout.write(f"  -> Band: {res_basic['performance_band']} (Expected: Basic)")
        assert res_basic["opi_score"] < config.proficient_cutoff
        assert res_basic["opi_score"] >= config.basic_cutoff
        assert res_basic["performance_band"] == "Basic"
        self.stdout.write(self.style.SUCCESS("  - Basic student alignment PASSED!"))

        # Test Case 4: Below Basic Student (55% accuracy, 5.0s response speed)
        # Expected OPI < 278 -> "Below Basic"
        res_bb = calculate_opi_score(55.0, 5.0)
        self.stdout.write(f"\n[TEST 4] Below Basic Student: Accuracy=55.0%, Speed=5.0s")
        self.stdout.write(f"  -> OPI Score: {res_bb['opi_score']}")
        self.stdout.write(f"  -> Band: {res_bb['performance_band']} (Expected: Below Basic)")
        assert res_bb["opi_score"] < config.basic_cutoff
        assert res_bb["performance_band"] == "Below Basic"
        self.stdout.write(self.style.SUCCESS("  - Below Basic student alignment PASSED!"))

        self.stdout.write("\n==================================================")
        self.stdout.write(self.style.SUCCESS("OSDE CCRA COMPLIANCE AUDIT PASSED successfully!"))
        self.stdout.write("==================================================")
