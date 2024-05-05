#!/usr/local/cs/bin/python3

import os, sys, zlib

"""
Implementation Notes on Strace

Used the following command to verify that the implementation does not invoke any Git commands.
`strace -f topo_order_commits.py 2> strace.log`

"""


class CommitNode:
    """
    CommitNode represents a single commit in a git repository.
    """
    
    def __init__(self, commit_hash, branches=[]):
        self.commit_hash = commit_hash
        self.parents = set()
        self.children = set()
        self.branches = branches


def validate_git():
    """
    Checks for the presence of a .git directory in the current or any parent directory.
    Changes the current working directory to the .git directory if found.
    Exits the program with an error message if not inside a Git repository.
    """
    # Traverse up the directory tree to find a '.git' directory
    origin_dir = os.getcwd()
    while os.getcwd() != '/' and '.git' not in os.listdir():
        os.chdir('..')
    
    # Check if '.git' exists in the current directory and restore original directory before exiting
    if '.git' not in os.listdir():
        sys.stderr.write('Not inside a Git repository\n')
        os.chdir(original_dir)
        exit(1)
    
    git_dir = os.path.join(os.getcwd(), '.git')
    # Verify '.git' is a directory and restore original directory before exiting
    if not os.path.isdir(git_dir):
        sys.stderr.write('Not inside a Git repository\n')
        os.chdir(origin_dir)
        exit(1)
    
    # Change working directory to the '.git' directory
    os.chdir(git_dir)
    


def get_branch_map():
    """
    Constructs a mapping from commit hashes to their corresponding branch names.
    Navigates to the 'refs/heads' directory within '.git', iterating over all branches
    to map each commit hash to a list of branch names that point to it.
    """
    # Dictionary to store the mapping of commit hashes to branch names.
    branch_map = {}
    # Change the working directory to the location of branch references.
    os.chdir('./refs/heads')
    
    # Traverse through all directories and files within 'refs/heads' to build the branch map.
    for root, dirs, files in os.walk("."):
        for name in files + dirs:
            # Construct the path for each branch reference and verify it's a file.
            branch_path = os.path.join(root, name)
            if os.path.isfile(branch_path):
                # Normalize the branch name by removing the leading './'.
                branch_name = branch_path[2:]
                
                # Open and read the commit hash pointed by the branch.
                with open(branch_name, 'r') as file:
                    hash_code = file.read().strip()  # Read the commit hash and remove any trailing newline.
                
                # Add or update the branch map with the commit hash and branch name.
                # This automatically handles the case of adding a branch name to an existing commit hash
                # or initializing a new list for a new commit hash.
                branch_map.setdefault(hash_code, []).append(branch_name)
    
    # Return to the '.git' directory after completing the operation.
    os.chdir('../../')
    
    return branch_map

def parent_hash(details):
    """
    Extracts and returns a list of parent commit hashes from a commit's detail string.
    """
    return [line.split(' ')[1] for line in details.split('\n') if line.startswith('parent')]


def get_parents(commit_hash):
    """
    Retrieves the list of parent commit hashes for a given commit hash.
    Assumes the current directory is the '.git/objects' directory.
    """
    # Split the hash to navigate to the object file
    dir_name, file_name = commit_hash[:2], commit_hash[2:]
    
    # Construct the path to the commit object and read it
    with open(os.path.join(dir_name, file_name), 'rb') as commit_file:
        content = zlib.decompress(commit_file.read()).decode()
    
    # Use the parent_hash function to extract parent commit hashes from details
    return parent_hash(content)


def commits_graph(branch_map):
    """
    Builds a directed DAG of commits from a branch map
    """
    
    # Navigate into the .git/objects directory to access commit objects.
    os.chdir('./objects')

    # Initialize a mapping of commit hashes to CommitNode objects.
    commit_nodes = {}
    # Identify commits that have no parents (root commits).
    root_commits = set()

    # Iterate through each commit hash provided in the branch map.
    for commit_hash in branch_map:
        # Check if this commit has already been processed.
        if commit_hash in commit_nodes:
            # Update the branches attribute of an existing commit node.
            commit_nodes[commit_hash].branches = branch_map[commit_hash]
        else:
            # Create a new CommitNode for unprocessed commits and initiate DFS.
            commit_nodes[commit_hash] = CommitNode(commit_hash, branch_map[commit_hash])
            stack = [commit_nodes[commit_hash]]
            while stack:
                current_node = stack.pop()
                parent_hashes = get_parents(current_node.commit_hash)

                # Add commit to root_commits if it has no parents.
                if not parent_hashes:
                    root_commits.add(current_node.commit_hash)

                # For each parent, create a CommitNode if it doesn't exist and set up parent-child relationships.
                for parent_hash in parent_hashes:
                    if parent_hash not in commit_nodes:
                        commit_nodes[parent_hash] = CommitNode(parent_hash)
                    current_node.parents.add(commit_nodes[parent_hash])
                    commit_nodes[parent_hash].children.add(current_node)
                    stack.append(commit_nodes[parent_hash])

    # Return to the parent directory of .git/objects.
    os.chdir('../')

    # Return the set of root commits and the comprehensive dictionary of commit nodes.
    return list(root_commits), commit_nodes


def topo_sorted_commits(root_commits, node_map):
    """
    Topologically sorts commits from a DAG, starting with root commits
    """
    
    # sorted_commits will hold the topologically sorted list of commit hashes.
    sorted_commits = []
    # visited keeps track of commits that have been visited to avoid cycles.
    visited = set()
    # stack is used instead of recursion for depth-first search.
    stack = root_commits.copy()
    
    while stack:
        current_commit = stack[-1]
        visited.add(current_commit)
        # Filter children not yet visited
        unvisited_children = [child for child in node_map[current_commit].children if child.commit_hash not in visited]
        
        if not unvisited_children:
            # If no unvisited children, pop from stack and add to sorted list
            stack.pop()
            sorted_commits.append(current_commit)
        else:
            # Otherwise, add the first unvisited child to the stack for processing
            stack.append(unvisited_children[0].commit_hash)
    
    return sorted_commits


def print_topo(topo_list, commit_node_map):
    """
    Prints the sorted commits with sticky ends
    """
    
    # Iterate through each commit hash in the topologically sorted list.
    for index in range(len(topo_list)):
        current_commit = topo_list[index]
        current_node = commit_node_map[current_commit]

        # Display the commit hash followed by branch names, if any.
        branch_info = " ".join(sorted(current_node.branches)) if current_node.branches else ""
        print(f"{current_commit} {branch_info}".strip())

        # Check and print relationships between non-consecutive parent and child commits.
        if index < len(topo_list) - 1:
            next_node = commit_node_map[topo_list[index + 1]]
            # If the next commit is not a direct child, print a sticky mark.
            if topo_list[index + 1] not in [parent.commit_hash for parent in current_node.parents]:
                parents = " ".join([parent.commit_hash for parent in current_node.parents])
                children = " ".join([child.commit_hash for child in next_node.children])
                print(f"{parents}=\n\n={children}")


def topo_order_commits():
    # Verify the presence of a Git repository; exit if not found.
    validate_git()
    # Map commit hashes to their corresponding branch names.
    commit_to_branch_map = get_branch_map()
    # Construct the DAG from branches, obtaining root commits and a map of CommitNodes.
    root_commits, commit_node_map = commits_graph(commit_to_branch_map)
    # Sort commits in topological way.
    sorted_commits = topo_sorted_commits(root_commits, commit_node_map)
    # Print the sorted commits with their branch name.
    print_topo(sorted_commits, commit_node_map)

                
if __name__ == '__main__':
    topo_order_commits()
