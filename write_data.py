def queue_in(queue, data):
    ret = None
    if len(queue) >= 3:
        ret = queue.pop(0)
    queue.append(data)
    return ret, queue


def write_txt(txt, ear, ear_vector):
    ret, ear_vector = queue_in(ear_vector, ear)
    if len(ear_vector) == 3:
        txt.write(str(ear_vector))
        txt.write("\n")
