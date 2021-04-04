CC = gcc
CFLAGS = -std=c99 -Wall -Werror


SRC_C = $(wildcard src/*.c)
# SRC_C = $(shell find $(SRCDIR) -type f -name *.$(SRCEXT))

OBJ_SRC = $(patsubst %.c, %.o, $(wildcard $(SRC_C)))
# OBJ_SRC = $(patsubst $(SRCDIR)/%, $(OBJDIR)/%, $(SRC_C:.$(SRCEXT)=.$(OBJEXT)))


app.out: $(OBJ_SRC)
	$(CC) -o $@ $^

test: app.out
	./$^ --file data/students_30.txt --numbilets 20 --parameter 424124

clean:
	$(RM) -rf *.out src/*.o
