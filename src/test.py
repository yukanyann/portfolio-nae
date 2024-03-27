from utils import load_yaml
from utils.google_cloud import execute


def main():
    template = load_yaml.load(r"src/data/default_nae_exp.yaml")
    for nae_type in template["野菜"]:
        audio_file=execute(template["野菜"][nae_type], "日本語", nae_type)
    


if __name__ == "__main__":
    main()
