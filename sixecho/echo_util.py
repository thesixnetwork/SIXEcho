def print_progress_bar(iteration,
                       total,
                       prefix='Progress',
                       suffix='Complete',
                       decimals=1,
                       length=100,
                       fill='='):
    """
    Call in a loop to create terminal progress bar
    Args:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(
        100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    tab_bar = fill * filled_length + '-' * (length - filled_length)
    print('\r%s |%s| %s%% %s' % (prefix, tab_bar, percent, suffix), end="\r")
    # Print New Line on Complete
    if iteration == total:
        print()
