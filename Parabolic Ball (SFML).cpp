/*

A simple Earth gravitation simulation.
Object takes off at an angle 45 degrees to the floor
and parabolically falls down with increasing speed.
(Without air resistance)

Created and codded by Arseny Zolotarev (Tuesday, 18 of July, 2023)

© 2019-2023 Zolars
  
*/


#include <SFML/Graphics.hpp>
#include <iostream>
#include <vector>
#include <math.h>
#include <time.h>

// Including resource files path

#include "ResourcePath.hpp"


using namespace std;
using namespace sf;


// Framerate class

class FPS{
public:
    FPS(): mFrame(0), mFps(0) {}
    unsigned int getFPS() const { return mFps; }
    
    void update(){
        if(mClock.getElapsedTime().asSeconds() >= 1.f){ mFps = mFrame; mFrame = 0; mClock.restart(); }
        mFrame++;
    }
    
private:
    unsigned int mFrame, mFps;
    Clock mClock;
};


// 2D Vector structure

struct vec {
    long double x, y;
    double length(){
        return sqrt(x * x + y * y);
    }
};


// 2D object structure

struct Object {
    vec pos, vel = {1, 0};
    double mass = 1.;
};


// Global varibales

const char *monitorText =
  "Delta time: %f\n"
  "Position: (%Lf, %Lf)\n"
  "Velocity: %Lf\n"
  "Projected velocity: (%Lf, %Lf)\n"
  "Mass: %Lf\n";
  // "Acceleration: %f\n"
  // "Acceleration (Ox, Oy): (%Lf, %Lf)\n";

double deltaTime = 0.01f, g = 9.81f;
float WIDTH = 800, HEIGHT = 800, H_WIDTH = WIDTH / 2, H_HEIGHT = HEIGHT / 2, ASPECT_RATIO = WIDTH / HEIGHT;


// Main function

int main() {
    // Creating environment
    
    Object obj;
    obj.pos.x = 0; obj.pos.y = 0;
    obj.mass = 2.25;
    obj.vel.x = 7.071; obj.vel.y = 7.071;
    vec a = {0, -g};
    
    // Trajectory vector

    VertexArray lines(LineStrip, 1);
    lines[0].position = Vector2f(H_WIDTH / 2, H_HEIGHT);
    int linesCount = 0;

    printf(monitorText, deltaTime, obj.pos, obj.vel.length(), obj.vel, obj.mass);
    
    // Creating window
    RenderWindow window(VideoMode(WIDTH, HEIGHT), "MIPH (visual)");
    window.setFramerateLimit(100);
//    window.setVerticalSyncEnabled(true);
    
    FPS fps;
    
    // Main cycle
        
    while (window.isOpen()){
        // User-input and Window events updating
        Event event;
        while (window.pollEvent(event)){
            if (event.type == Event::Closed)
                window.close();
            
            if (event.type == Event::KeyPressed){
                if (Keyboard::isKeyPressed(Keyboard::P))
                    printf(monitorText, deltaTime, obj.pos, obj.vel.length(), obj.vel, obj.mass);
                if (Keyboard::isKeyPressed(Keyboard::R)){
                    obj.pos.x = 0; obj.pos.y = 0;
                    obj.mass = 2.25;
                    obj.vel.x = 7.071; obj.vel.y = 7.071;
                    a = {0, -g};
                    
                    lines.clear();
                    lines.append(Vector2f(H_WIDTH / 2, H_HEIGHT));
                    linesCount = 0;
                }
            }
              
            // Mouse events
            if (event.type == Event::MouseButtonPressed){
                string filename = resourcePath() + "../../../screenshot.png";
                Texture texture;
                texture.create(window.getSize().x, window.getSize().y);
                texture.update(window);
                if (texture.copyToImage().saveToFile(filename)) printf("screenshot saved to %s\n", filename.c_str());
            }
        }
        

        // Drawing
        window.clear(Color(200, 200, 200));
        
        lines.append(sf::Vector2f(obj.pos.x * 20 + H_WIDTH / 2, H_HEIGHT - obj.pos.y * 20));
        lines[linesCount].color = Color(255, 100, 100);
        linesCount++;
        CircleShape ball(5, 10);
        ball.setPosition(obj.pos.x * 20 + H_WIDTH / 2, H_HEIGHT - obj.pos.y * 20);
        
        window.draw(ball);
        window.draw(lines);

        // Environments updating
        
        a = {0, -g};
        obj.vel.x += a.x * deltaTime; obj.vel.y += a.y * deltaTime;
        obj.pos.x += obj.vel.x * deltaTime; obj.pos.y += obj.vel.y * deltaTime;

        // Screen updating

        fps.update();
        window.setTitle("MIPH (visual) fps: " + to_string(fps.getFPS()));
        window.display();
    }

    return 0;
}
