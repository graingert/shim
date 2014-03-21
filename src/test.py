from random import randint, sample, seed
from optparse import OptionParser
import os, sys
# intialize option fields
def opt_init(parser):
    parser.add_option('-s', dest='seed',
                      type='int', help='seed value for random number generator')
    parser.add_option('-c', dest='snapshotcount', default=5,
                      type='int', help='number of snapshots')
    parser.add_option('-p', dest='processcount', default=4,
                      type='int', help='number of snapshots')


# similar to application logic, generate name depending on integer argument
def generate_client_info(count):
    info = ''
    info += chr(ord('A') + count % 26)
    count -= count % 26
    numA = (count / 26, 1)[count == 26]
    info = (numA * 'A') + info
    return info

# generate message instruction
def generate_message(process_count):
    a = generate_client_info(randint(0,process_count - 1))
    b = a
    while b == a:
        b = generate_client_info(randint(0,process_count - 1))
    widget_count, money_count = randint(1, 5), randint(1, 10)
    return '%s %s %d %d' % (a, b, widget_count, money_count)

# build a random routine of instructions and snapshots with 50 messages
def build_random_routine(snapshot_count, process_count):
    snapshot_count = (49, snapshot_count)[snapshot_count < 49]
    snapshot_locations = sorted(sample(xrange(0,49), snapshot_count))
    messages = ['sleep']
    count = 1
    for i in range(50):
        messages.append(generate_message(process_count))
        if i in snapshot_locations:
            messages.append('snapshot '+ str(count))
            count += 1
    messages.append('sleep')
    messages.append('kill all')
    return messages

# generate an instruction file to pipe to application
def create_instruction_file(snapshot_count, process_count):
    with open('instructions.txt', 'w+') as f:
        f.write('\n'.join(build_random_routine(snapshot_count, process_count)))
# call all test subroutines and pipe to app.py
if __name__ == '__main__':
    parser = OptionParser()
    opt_init(parser)
    (options, args) = parser.parse_args() processcount
    if options.seed:
        seed(options.seed)
    if options.processcount:
        print options.processcount
    create_instruction_file(options.snapshotcount, options.processcount)
    instruction = 'python app.py -n %d < instructions.txt' % (options.processcount)
    os.system(instruction)

