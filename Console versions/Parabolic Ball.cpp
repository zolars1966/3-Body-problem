/*

A simple Earth gravitation simulation. 
Object takes off at an angle 45 degrees to the floor
and parabolically falls down with increasing speed.
(Without air resistance)

Created and codded by Arseny Zolotarev (Tuesday, 18 of July, 2023)

© 2019-2023 Zolars
  
*/

#include <iostream>
#include <math.h>


using namespace std;


struct vec {
	long double x, y;
	double length(){
		return sqrt(x * x + y * y);
	}
};


struct Object {
	vec pos, vel = {1, 0};
	double mass = 1.;
};


const char *monitorText =
  "Delta time: %f\n"
  "Position: (%Lf, %Lf)\n"
  "Velocity: %Lf\n"
  "Projected velocity: (%Lf, %Lf)\n"
  "Mass: %Lf\n";
  // "Acceleration: %f\n"
  // "Acceleration (Ox, Oy): (%Lf, %Lf)\n";

double deltaTime = 0.1f, g = 9.81f;


int main(){
	Object obj;
	obj.pos.x = 0; obj.pos.y = 0;
	obj.mass = 2.25;
	obj.vel.x = 7.071, obj.vel.y = 7.071;
	vec a = {0, -g};
	bool r = 1;

	printf(monitorText, deltaTime, obj.pos, obj.vel.length(), obj.vel, obj.mass);

	while (deltaTime){
		a = {0, -g};
		obj.vel.x += a.x * deltaTime; obj.vel.y += a.y * deltaTime;
		obj.pos.x += obj.vel.x * deltaTime; obj.pos.y += obj.vel.y * deltaTime;

		printf(monitorText, deltaTime, obj.pos, obj.vel.length(), obj.vel, obj.mass);
		cin >> deltaTime;
	}

	return 0;
}
