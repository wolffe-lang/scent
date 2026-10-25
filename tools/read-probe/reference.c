/* Original measurement adapter; libc is a black-box API, never source input.
   Not linked into scent. Same 96 KiB reads; reused buffer and memchr controls. */
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
int main(int argc, char **argv) {
    if (argc != 3) return 2;
    int fd = open(argv[2], O_RDONLY);
    if (fd < 0) return 2;
    unsigned char buf[98304];
    long long bytes = 0, lines = 0;
    ssize_t n;
    while ((n = read(fd, buf, sizeof buf)) > 0) {
        bytes += n;
        if (!strcmp(argv[1], "scan")) {
            const unsigned char *p = buf, *end = buf + n;
            while (p < end && (p = memchr(p, '\n', (size_t)(end - p)))) {
                ++lines; ++p;
            }
        }
    }
    if (n < 0 || close(fd)) return 2;
    printf("%lld %lld\n", bytes, lines);
    return 0;
}
