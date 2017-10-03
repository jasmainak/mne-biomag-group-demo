import time
from importlib import import_module
from memory_profiler import memory_usage
import matplotlib.pyplot as plt

subject_id = 1

filenames = ['02-python_filtering', '03-run_extract_events',
             '04-run_ica', '05-make_epochs', '06-make_evoked',
             '07-time_frequency', '08-run_time_decoding',
             '12-make_forward', '13-make_inverse', '14-group_average_source']

funcs = ['run_filter', 'run_events', 'run_ica', 'run_epochs',
         'run_evoked', 'run_time_frequency', 'run_time_decoding',
         'run_forward', 'run_inverse', 'morph_stc']

times, memory = list(), list()
for fname, func in zip(filenames, funcs):
    t1 = time.time()
    print('Importing %s' % fname)
    mod = import_module(fname)
    func, args, kwargs = getattr(mod, func), (subject_id, ), {}
    mem = memory_usage((func, args, kwargs), max_usage=True)
    times.append(time.time() - t1)
    memory.append(mem)

# Plot memory and time taken
plt.pie(memory, labels=funcs)
plt.title('Memory usage')

plt.figure()
plt.pie(times, labels=funcs)
plt.title('Time taken')
