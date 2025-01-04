def overwrite_at(line_number, text):
    # Move the cursor to the specified line relative to the current position
    print(f"\033[{line_number}F", end="")  # Move up to the target line
    print(f"\033[K{text}", end="\n", flush=True)  # Clear the line and print new content


def proc_file_path(path):
    path = path.removesuffix('.mp3')
    path = path.removesuffix('.wav')
    path = path.split('/')[-2:]
    return (f'\n     {path[0]}/\n          {path[1]}')