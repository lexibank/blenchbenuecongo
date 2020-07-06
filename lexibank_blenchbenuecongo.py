import attr
from clldutils.path import Path
from pylexibank import Concept
from pylexibank import Dataset as BaseDataset
from pylexibank.forms import FormSpec


@attr.s
class CustomConcept(Concept):
    French = attr.ib(default=None)


class Dataset(BaseDataset):
    dir = Path(__file__).parent
    id = "blenchbenuecongo"
    concept_class = CustomConcept

    form_spec = FormSpec(
        replacements=[("[", ""), ("]", "")],
        brackets={"(": ")", "[": "]"},
        separators=(",", ";"),
        normalize_unicode="NFC",
        missing_data=("-", "- -", "--", "----"),
    )

    def cmd_makecldf(self, args):
        args.writer.add_sources()
        args.writer.add_concepts(id_factory=lambda d: d.number.replace(".", "-"))
        languages = args.writer.add_languages()

        for p in self.raw_dir.glob("*.csv"):
            lid = p.stem.split("-")[1]
            if lid in languages:
                for item in self.raw_dir.read_csv(p, delimiter=",", dicts=True):
                    if item["Phonetic"]:

                        args.writer.add_forms_from_value(
                            Language_ID=lid,
                            Parameter_ID=item["BNC ID"].replace(".", "-"),
                            Value=item["Phonetic"],
                            Source=["Williamson1968", "Williamson1973"],
                        )
