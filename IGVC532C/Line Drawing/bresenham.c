#include <GL/glut.h>
#include <stdio.h>

int n;
int p[100][2];
int WIDTH = 640, HEIGHT = 480;

void Init()
{
  glClearColor(1.0,1.0,1.0,0);
  glColor3f(0.0,0.0,0.0);
  // gluOrtho2D(-WIDTH/2 , WIDTH/2 , -HEIGHT/2 , HEIGHT/2);
  gluOrtho2D(0, WIDTH, 0, HEIGHT);
}

void putPixel(int x, int y) {
	glVertex2i(x, y);
}

void bresenhamLine() {
	int dx, dy, e;
	int incx, incy, inc1, inc2;
	int x,y;

 	glClear(GL_COLOR_BUFFER_BIT);
	glBegin(GL_POINTS);
	for(int i = 0; i < n; i += 2) {
		dx = abs(p[i+1][0] - p[i][0]);
		dy = abs(p[i+1][1] - p[i][1]);
		incx = (p[i+1][0] > p[i][0]) ? 1 : -1;
		incy = (p[i+1][1] > p[i][1]) ? 1 : -1;
		x = p[i][0];
		y = p[i][1];
		putPixel(x, y);
		
		if(dx > dy) {
			inc1 = 2*dy;
			inc2 = 2*(dy - dx);
			e = 2*dy - dx;
			for(int j = 0; j < dx; j++) {
				if (e < 0) {
					e += inc1;
				} else {
					y += incy;
					e += inc2;
				}
				x += incx;
				putPixel(x, y);
			}
		}
		else {
			inc1 = 2*dx;
			inc2 = 2*(dx - dy);
			e = 2*dx - dy;
			for(int j = 0; j < dy; j++) {
				if (e < 0) {
					e += inc1;
				} else {
					x += incx;
					e += inc2;
				}
				y += incy;
				putPixel(x, y);
			}
		}
	}
	glEnd();
	glFlush();
}

int main(int argc, char **argv) {

	scanf("%d", &n);
	n = 2*n;

	for(int i = 0; i < n; i++) {
		scanf("%d%d", &p[i][0], &p[i][1]);
	}

	glutInit(&argc,argv);
	glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB);
	glutInitWindowPosition(0,0);
	glutInitWindowSize(WIDTH,HEIGHT);
	glutCreateWindow("Bresenham's Line Drawing");
	Init();
	glutDisplayFunc(bresenhamLine);
	glutMainLoop();
	return 0;
}




/*

dx = p[j+1][0] - p[j][0];
		dy = p[j+1][1] - p[j][1];

		if (dx < 0) dx = -dx;
		if (dy < 0) dy = -dy;
		incx = 1;
		if (p[j+1][0] < p[j][0]) incx = -1;
		incy = 1;
		if (p[j+1][1] < p[j][1]) incy = -1;
		x = p[j][0]; y = p[j][1];
		if (dx > dy) {
			putPixel(x, y);
			e = 2 * dy-dx;
			inc1 = 2*(dy-dx);
			inc2 = 2*dy;
			for (i=0; i<dx; i++) {
				if (e >= 0) {
					y += incy;
					e += inc1;
				}
				else
					e += inc2;
				x += incx;
				putPixel(x, y);
			}

		} else {
			putPixel(x, y);
			e = 2*dx-dy;
			inc1 = 2*(dx-dy);
			inc2 = 2*dx;
			for (i=0; i<dy; i++) {
				if (e >= 0) {
					x += incx;
					e += inc1;
				}
				else
					e += inc2;
				y += incy;
				putPixel(x, y);
			}
		}

*/