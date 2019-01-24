#include <stdio.h>
#include <math.h>
#include <GL/glut.h>

int n;
double p[100][2];
int WIDTH = 640, HEIGHT = 480;

void putPoint(double x, double y) {
  glVertex2d((int)(x+.5), (int) (y+.5));
}

void LineDDA()
{
  while(1) {

  glClear(GL_COLOR_BUFFER_BIT);
  glBegin(GL_POINTS);
    for(int i = 0; i < n; i += 2) {
      double dx=(p[i+1][0]-p[i][0]);
      double dy=(p[i+1][1]-p[i][1]);
      double steps;
      float xInc,yInc,x=p[i][0],y=p[i][1];

      steps=(abs(dx)>abs(dy))?(abs(dx)):(abs(dy));
      xInc=dx/(float)steps;
      yInc=dy/(float)steps;
      glVertex2d(x,y);

      int k;
      for(k=0;k<steps;k++) {
        x+=xInc;
        y+=yInc;
        putPoint(x, y);
      }
    }

    glEnd();
    glFlush();

    for(int i = 0; i < n; i++) {
      p[i][0] = ((int)(p[i][0]+.5) > WIDTH)? 0 : (p[i][0]+.1);
    }
  }
}

void Init()
{
  glClearColor(1.0,1.0,1.0,0);
  glColor3f(0.0,0.0,1.0);
  //gluOrtho2D(-WIDTH/2 , WIDTH/2 , -HEIGHT/2 , HEIGHT/2);
  gluOrtho2D(0, WIDTH, 0, HEIGHT);
  //gluOrtho2D(0, 200, 0, 200);
}
int main(int argc, char **argv)
{
  
  scanf("%d", &n);
  n = 2*n;
  for(int i = 0; i < n; i++) {
    scanf("%lf%lf", &p[i][0], &p[i][1]);
  }

  glutInit(&argc,argv);
  glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB);
  glutInitWindowPosition(0,0);
  glutInitWindowSize(WIDTH,HEIGHT);
  glutCreateWindow("DDA_Line");
  Init();
  glutDisplayFunc(LineDDA);
  glutMainLoop();

  return 0;
}