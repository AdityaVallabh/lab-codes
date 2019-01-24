#include <stdio.h>
#include <math.h>
#include <GL/glut.h>
#define N 3
#define PI 3.14159265

int WIDTH = 800, HEIGHT = 800;

typedef struct {
	int x, y;
} Point;

void multiply(double mat1[][N], int mat2[], int res[])
{
    int i, j, k;
    for (i = 0; i < N; i++)
    {
        res[i] = 0;
        for (k = 0; k < N; k++) {
            res[i] += (int) 1.0*mat1[i][k]*mat2[k];
        }
    }
}

void drawLine(Point p1, Point p2, int *color) {
 	glBegin(GL_LINES);
 	glColor3f(color[0], color[1], color[2]);
	glVertex2d((int)(p1.x+.5), (int) (p1.y+.5));
	glVertex2d((int)(p2.x+.5), (int) (p2.y+.5));
	glEnd();
}

Point translate(Point p, int tx, int ty) {
	Point q;
	double mat1[3][3] = {
		{1, 0, tx},
		{0, 1, ty},
		{0, 0, 1},
	};
	int mat2[3] = {p.x, p.y, 1}, res[3];
	multiply(mat1, mat2, res);
	q.x = res[0];
	q.y = res[1];
	// q.x = p.x + tx;
	// q.y = p.y + ty;
	return q;
}

Point rotate(Point p, Point c, double th) {
	Point q;
	th = (int) 1.0*th*PI/180;

	double mat1[3][3] = {
		{cos(th), -sin(th), 0},
		{sin(th), cos(th), 0},
		{0, 0, 1}
	};
	int mat2[3] = {p.x, p.y, 1}, res[3];
	multiply(mat1, mat2, res);
	q.x = res[0];
	q.y = res[1];
	// q.x = (int) 1.0*(p.x - c.x)*cos(th) - 1.0*(p.y - c.y)*sin(th) + c.x;
	// q.y = (int) 1.0*(p.x - c.x)*sin(th) + 1.0*(p.y - c.y)*cos(th) + c.y;
	return q;
}

Point scale(Point p, double f) {
	Point q;
	double mat1[3][3] = {
		{f, 0, 0},
		{0, f, 0},
		{0, 0, f}
	};
	int mat2[3] = {p.x, p.y, 1}, res[3];
	multiply(mat1, mat2, res);
	q.x = res[0];
	q.y = res[1];
	// q.x = (int) p.x * f;
	// q.y = (int) p.y * f;
	return q;
}

void myDisplayFunc() {
	int BLUE[3] = {0,0,1}, RED[3] = {1,0,0};
    glClear(GL_COLOR_BUFFER_BIT);

    glBegin(GL_LINES);
    Point p1; p1.x = p1.y = 0;
    Point p2 = translate(p1, 200, 0);
    Point p3 = rotate(translate(p2, -100, 0), p1, 90);
    drawLine(p1, p2, RED);
    drawLine(p1, p3, RED);
    drawLine(p2, p3, RED);

    Point p4 = rotate(scale(p3, sqrt(10)), p1, 18.435);
    Point p5 = rotate(scale(p3, sqrt(2)), p1, 135);
    drawLine(p1, p4, BLUE);
	drawLine(p1, p5, BLUE);
	drawLine(p4, p5, BLUE);
    glEnd();

    glFlush();
}


void Init()
{
  glClearColor(1.0,1.0,1.0,0);
  glColor3f(0.0,0.0,1.0);
  gluOrtho2D(-WIDTH/2 , WIDTH/2 , -HEIGHT/2 , HEIGHT/2);
  //gluOrtho2D(0, WIDTH, 0, HEIGHT);
  //gluOrtho2D(0, 200, 0, 200);
}
int main(int argc, char **argv)
{
    glutInit(&argc,argv);
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB);
    glutInitWindowPosition(0,0);
    glutInitWindowSize(WIDTH,HEIGHT);
    glutCreateWindow("Transformations");
    Init();
    glutDisplayFunc(myDisplayFunc);
    glutMainLoop();

    return 0;
}
