import os
import sys
import subprocess


def logger(log):
    log_header = ">>>>>>>>>> "
    print "{0}{1}".format(log_header, log)


def clean_repository(status_output):
    start = status_output.find("Untracked files:")
    if start >= 0:
        for f in status_output[start:].split("\n\n")[1].split():
            logger("delete: {0}".format(f))
            os.remove(f)
    logger("git checkout -f")
    output = subprocess.check_output(["git", "checkout", "-f"])
    print output


def check_repository_status():
    logger("git status")
    output = subprocess.check_output(["git", "status"])
    print output

    if "working directory clean" not in output:
        user_in = ""
        while not user_in:
            user_in = raw_input("Working repository is NOT clean, Do you want to clean up it? (y/n):")
        if user_in == 'y':
            clean_repository(output)
            check_repository_status()
        else:
            sys.exit(1)


def find_all_repositories(path, out_list):
    dir_count = 0
    file_count = 0
    for f in sorted(os.listdir(path)):
        if os.path.isdir(os.path.join(path, f)):
            find_all_repositories(os.path.join(path, f), out_list)
            dir_count += 1
        elif os.path.isfile(os.path.join(path, f)):
            file_count += 1

    if dir_count == 0 and file_count > 0:
        out_list.append(path)


def apply_repository_patches(message_header, patch_path, workspace_path, repository):
    logger("Applying repository: {0}".format(repository))
    workspace_repository_path = os.path.normpath(os.path.join(workspace_path, repository))
    patch_repository_path = os.path.normpath(os.path.join(patch_path, repository))

    logger("Change dir to {0}".format(workspace_repository_path))
    os.chdir(workspace_repository_path)

    check_repository_status()

    for patch in sorted(os.listdir(patch_repository_path)):

        patch_full_path = os.path.join(patch_repository_path, patch)

        logger("git apply {0}".format(patch_full_path))

        p = subprocess.Popen(["git", "apply", patch_full_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        print out
        print err
        if p.returncode != 0:
            logger("Apply failed: repository path: {0}".format(workspace_repository_path))
            for line in err.split("\n"):
                if line.startswith("error: patch failed:"):
                    logger(line)
                    target_file, l_num = line.split()[3].split(':')
                    target_file_full_path = os.path.join(workspace_repository_path, target_file)
                    logger("Open files in gedit:")
                    logger(target_file_full_path)
                    logger(patch_full_path)
                    subprocess.Popen(["gedit", target_file_full_path, "+{0}".format(l_num)])
                    subprocess.Popen(["gedit", patch_full_path])

            user_in = ""
            while not user_in:
                user_in = raw_input("Auto apply failed, please resolve it manually, then input 'go':")
            if user_in != 'go':
                sys.exit(1)

        logger("Apply OK, delete patch file: {0}".format(patch_full_path))
        os.remove(patch_full_path)

        logger("git add -A")
        subprocess.check_call(["git", "add", "-A"])

        commit_message = "[{0}] {1}".format(message_header, patch)
        logger("git commit -m '{0}'".format(commit_message))
        subprocess.check_call(["git", "commit", "-m", commit_message])

    logger("git push origin HEAD:refs/for/e1_dev")
    subprocess.check_call(["git", "push", "origin", "HEAD:refs/for/e1_dev"])


def main(argv):
    if len(argv) == 3:
        message_header = argv[1]
        patch_path = argv[2]
        workspace_path = os.path.abspath(".")
    elif len(argv) == 4:
        message_header = argv[1]
        patch_path = argv[2]
        workspace_path = argv[3]
    else:
        print "Auto patch: apply a group of patches automatically"
        print "usage: python auto_patch.py HEADER PATCH_PATH [WORKSPACE]"
        print "HEADER:     This string will as a prefix of your commit message"
        print "PATCH_PATH: The root directory of patch path"
        print "WORKSPACE:  Your workspace path."
        print "            This is optional if you run this script on your workspace root directory"
        sys.exit(1)

    logger("Commit message header: {0}".format(message_header))
    logger("Patch path: {0}".format(patch_path))
    logger("Workspace path: {0}".format(workspace_path))

    logger("Change dir to {0}".format(patch_path))
    os.chdir(patch_path)

    logger("Finding all repositories ...")
    repositories_list = []
    find_all_repositories(".", repositories_list)
    logger("[found repositories]:")
    for repo in repositories_list:
        logger(repo)

    logger("Change dir to {0}".format(workspace_path))
    os.chdir(workspace_path)
    for repo in repositories_list:
        apply_repository_patches(message_header, patch_path, workspace_path, repo)

    logger("Change dir to {0}".format(workspace_path))
    os.chdir(workspace_path)

    logger("All works done.")


if __name__ == "__main__":
    main(sys.argv)
