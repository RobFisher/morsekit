PREFIX=/usr/local

ALL: cwtext cwpcm cwmm

install: ALL
	install -sc cwtext ${PREFIX}/bin
	install -sc cwpcm ${PREFIX}/bin
	install -sc cwmm ${PREFIX}/bin

cwmm: cwmm.o morse.o
	${CC} ${CFLAGS} -o cwmm $^
	
cwpcm: cwpcm.o morse.o pcm.o
	${CC} ${CFLAGS} -o cwpcm -lm $^

cwtext: cwtext.o morse.o
	${CC} ${CFLAGS} -o cwtext  $^

testpcm: testpcm.o pcm.o
	${CC} ${CFLAGS} -o testpcm -lm $^

cwpcm.o: cwpcm.c morse.h pcm.h
	${CC} ${CFLAGS} -c cwpcm.c

cwtext.o: cwtext.c morse.h
	${CC} ${CFLAGS} -c cwtext.c

morse.o: cw.h morse.h morse.h
	${CC} ${CFLAGS} -c morse.c

pcm.o: pcm.c pcm.h
	${CC} ${CFLAGS} -c pcm.c

testpcm.o: testpcm.c pcm.c pcm.h
	${CC} ${CFLAGS} -c testpcm.c

cw.h: gencw.py
	python gencw.py > cw.h

test.wav: cwpcm
	echo 123test | ./cwpcm | sox -r 8000 -bu -t raw - test.wav

clean:
	-rm -f *.o cwmm cwpcm cwtext core cw.h test.wav
