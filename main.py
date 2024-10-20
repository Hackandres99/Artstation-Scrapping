from scrapping.execution import load_config, run_action


def main():
    config = load_config('config.yaml')
    run_action(config)


if __name__ == '__main__':
    main()
