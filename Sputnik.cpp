/*

A simple Earth gravitation simulation.
Sputnik moving around the planet
(no effects to the planet applied).

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
//   "Acceleration: %f\n"
//   "Acceleration (Ox, Oy): (%Lf, %Lf)\n";

double deltaTime = 0.005f, g = 9.81f;
float WIDTH = 800, HEIGHT = 800, H_WIDTH = WIDTH / 2, H_HEIGHT = HEIGHT / 2, ASPECT_RATIO = WIDTH / HEIGHT;


// Main function
int main() {
    // Creating environment
    Object planet, sputnik;
    
    planet.mass = 27;
    planet.vel.x = 0; planet.vel.y = 0;
    
    sputnik.pos.x = 15; sputnik.pos.y = 0;
    sputnik.mass = 1;
    sputnik.vel.x = 0; sputnik.vel.y = 5;

    vec a = {planet.mass / -sputnik.pos.x, 0};
    
    // Trajectory vector
    VertexArray lines(LineStrip, 1);
    lines[0].position = Vector2f(H_WIDTH + 300, H_HEIGHT);
    int linesCount = 0;

    printf(monitorText, deltaTime, sputnik.pos, sputnik.vel.length(), sputnik.vel, sputnik.mass);
    
    // Creating window
    RenderWindow window(VideoMode(WIDTH, HEIGHT), "MIPH (visual)");
//    window.setFramerateLimit(100);
//    window.setVerticalSyncEnabled(true);
    
    FPS fps;
    Clock dTime;
    
    // Main cycle
    while (window.isOpen()){
        // User-input and Window events updating
        Event event;
        while (window.pollEvent(event)){
            if (event.type == Event::Closed)
                window.close();
            
            if (event.type == Event::KeyPressed){
                if (Keyboard::isKeyPressed(Keyboard::P))
                    printf(monitorText, deltaTime, sputnik.pos, sputnik.vel.length(), sputnik.vel, sputnik.mass);
                if (Keyboard::isKeyPressed(Keyboard::R) || Keyboard::isKeyPressed(Keyboard::D)){
                    if (Keyboard::isKeyPressed(Keyboard::D)){ cout << "Write new time period: "; cin >> deltaTime; };

                    planet.mass = 27;
                    planet.vel.x = 0; planet.vel.y = 0;
                    
                    sputnik.pos.x = 15; sputnik.pos.y = 0;
                    sputnik.mass = 1;
                    sputnik.vel.x = 0; sputnik.vel.y = 5;

                    a = {planet.mass / -sputnik.pos.x, 0};
                    
                    lines.append(Vector2f(H_WIDTH, H_HEIGHT));
                    lines[linesCount++].color = Color(200, 200, 200);
                    lines[linesCount].color = Color(200, 200, 200);
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
        
        lines.append(sf::Vector2f(sputnik.pos.x * 20 + H_WIDTH, H_HEIGHT - sputnik.pos.y * 20));
        lines[++linesCount].color = Color(255, 100, 100);
        CircleShape ball(5, 10);
        ball.setPosition(sputnik.pos.x * 20 + H_WIDTH, H_HEIGHT - sputnik.pos.y * 20);
        
        window.draw(ball);
        window.draw(lines);

        // Environments updating
        if (dTime.getElapsedTime().asSeconds() >= deltaTime){
            a = {planet.mass * sputnik.pos.x / -pow(sputnik.pos.length(), 2), planet.mass * sputnik.pos.y / -pow(sputnik.pos.length(), 2)};
            sputnik.vel.x += a.x * deltaTime; sputnik.vel.y += a.y * deltaTime;
            sputnik.pos.x += sputnik.vel.x * deltaTime; sputnik.pos.y += sputnik.vel.y * deltaTime;
            dTime.restart();
        }

        // Screen updating
        fps.update();
        window.setTitle("MIPH (visual) fps: " + to_string(fps.getFPS()));
        window.display();
    }

    return 0;
}
