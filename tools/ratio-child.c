/* Run one command and report what it cost, from a parent that holds almost nothing.
 *
 *   ratio-child OUT ERR PROGRAM [ARG...]
 *
 * The child's stdin is /dev/null, its stdout OUT and its stderr ERR (both created
 * or truncated). One line goes to this program's stdout:
 *
 *   status=S user_us=U sys_us=Y wall_us=W maxrss_kb=K minflt=F
 *
 * S is the exit status, or 128 plus the signal. Linux carries a process's peak
 * resident size across exec, so the parent is static and small, and its own floor
 * is read by running `ratio-child OUT ERR --floor`, which reports a child that
 * execs nothing.
 */
#include <errno.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/resource.h>
#include <sys/time.h>
#include <sys/wait.h>
#include <time.h>
#include <unistd.h>

static long long micros(struct timeval t) { return (long long)t.tv_sec * 1000000LL + t.tv_usec; }

int main(int argc, char **argv) {
    if (argc < 4) {
        fprintf(stderr, "usage: ratio-child OUT ERR PROGRAM [ARG...] | ratio-child OUT ERR --floor\n");
        return 2;
    }
    int floor = strcmp(argv[3], "--floor") == 0;
    struct timespec t0, t1;
    clock_gettime(CLOCK_MONOTONIC, &t0);
    pid_t pid = fork();
    if (pid < 0) {
        perror("ratio-child: fork");
        return 2;
    }
    if (pid == 0) {
        int in = open("/dev/null", O_RDONLY);
        int out = open(argv[1], O_WRONLY | O_CREAT | O_TRUNC, 0644);
        int err = open(argv[2], O_WRONLY | O_CREAT | O_TRUNC, 0644);
        if (in < 0 || out < 0 || err < 0 || dup2(in, 0) < 0 || dup2(out, 1) < 0 || dup2(err, 2) < 0) _exit(126);
        close(in);
        close(out);
        close(err);
        if (floor) _exit(0);
        execv(argv[3], argv + 3);
        _exit(127);
    }
    int status = 0;
    struct rusage ru;
    if (wait4(pid, &status, 0, &ru) != pid) {
        perror("ratio-child: wait4");
        return 2;
    }
    clock_gettime(CLOCK_MONOTONIC, &t1);
    int code = WIFEXITED(status) ? WEXITSTATUS(status) : 128 + WTERMSIG(status);
    long long wall = (long long)(t1.tv_sec - t0.tv_sec) * 1000000LL + (t1.tv_nsec - t0.tv_nsec) / 1000;
    printf("status=%d user_us=%lld sys_us=%lld wall_us=%lld maxrss_kb=%ld minflt=%ld\n", code, micros(ru.ru_utime),
           micros(ru.ru_stime), wall, ru.ru_maxrss, ru.ru_minflt);
    return 0;
}
