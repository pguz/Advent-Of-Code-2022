# Day 07: No Space Left On Device


class Dir:
    def __init__(self, parent) -> None:
        self.parent = parent
        self.files = []
        self.dirs = {}
        self.size = 0

    def add_dir(self, dir_name) -> None:
        assert dir_name not in self.dirs
        self.dirs[dir_name] = Dir(parent=self)

    def add_file(self, file_name: str, size: int) -> None:
        assert file_name not in self.files
        self.files.append(file_name)
        self.size += size

        parent = self.parent
        while parent:
            parent.size += size
            parent = parent.parent

    def enter(self, dir_name):
        assert dir_name in self.dirs
        return self.dirs[dir_name]

    def exit(self):
        return self.parent


def parse_file(fd):
    return fd.readlines(),

def _build_filesystem_tree(root_dir, outputs):
    current_dir = root_dir
    for output in outputs:
        if output.startswith('$ cd'):
            _, _, dir_name = output.split()
            if dir_name == "..":
                current_dir = current_dir.exit()
            else:
                current_dir = current_dir.enter(dir_name)
        elif output.startswith('$ ls'):
            pass
        elif output.startswith('dir'):
            _, dir_name = output.split()
            current_dir.add_dir(dir_name)
        else:
            file_size, file_name = output.split()
            current_dir.add_file(file_name, int(file_size))

def dir_size_less_than_100000(outputs):
    def count_size(dir_):
        size = 0
        if dir_.size <= 100000:
            size += dir_.size
        return size + sum(count_size(d) for d in dir_.dirs.values())

    root_dir = Dir(parent=None)
    _build_filesystem_tree(root_dir, outputs=outputs[1:])
    return count_size(root_dir)

def dir_to_delete(outputs):
    disc_space = 70000000
    space_needed = 30000000

    def find_space_to_delete(dir_, space_to_release):
        childern_dirs = dir_.dirs.values()
        spaces = [space for d in childern_dirs if (space := find_space_to_delete(d, space_to_release))]
        if dir_.size >= space_to_release:
            spaces.append(dir_.size)
        if spaces:
            return min(spaces)
        return None

    root_dir = Dir(parent=None)
    _build_filesystem_tree(root_dir, outputs=outputs[1:])

    space_to_release = space_needed - (disc_space - root_dir.size)
    assert space_to_release >= 0
    return find_space_to_delete(root_dir, space_to_release)

solution_function_01 = dir_size_less_than_100000
solution_function_02 = dir_to_delete
