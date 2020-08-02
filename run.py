#!/usr/bin/env python
import os
import argparse

def run():
    """ Reuse the Procfile to start the dev server """
    with open("Procfile", "r") as f:
        command = f.read().strip()

    command = command.replace("web: ", "")
    command += " --reload"
    os.system(command)

def deploy():
    os.system("git push dokku master")

def dependencies():
    os.system("pip-compile --upgrade requirements.in")
    os.system("pip-compile --upgrade requirements-dev.in")
    os.system("pip-sync requirements-dev.txt")

def get_universities():
    os.system("curl https://raw.githubusercontent.com/Hipo/university-domains-list/master/world_universities_and_domains.json --output universities.json")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--deploy', action="store_true", required=False)
    parser.add_argument('--deps', action="store_true", required=False)
    parser.add_argument('--get_universities', action="store_true", required=False)
    args = parser.parse_args()

    if args.deploy:
        deploy()
    elif args.deps:
        dependencies()
    elif args.get_universities:
        get_universities()
    else:
        run()


if __name__ == '__main__':
    main()
