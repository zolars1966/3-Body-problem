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
        if (mClock.getElapsedTime().asSeconds() >= 1.f){ mFps = mFrame; mFrame = 0; mClock.restart(); }
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
    vec pos, vel = {1., 0.}, a = {0., 0.};
    double mass = 1.;
};


double dist(vec v1, vec v2){
    return sqrt((v1.x - v2.x)*(v1.x - v2.x) + (v1.y - v2.y)*(v1.y - v2.y));
}

double dist_S(vec v1, vec v2){
    return (v1.x - v2.x)*(v1.x - v2.x) + (v1.y - v2.y)*(v1.y - v2.y);
}


// Global varibales
double tickRate = 60, deltaTime = 0.005f, coeff = 0.001, simTime = 0;
float WIDTH = 800, HEIGHT = 800, H_WIDTH = WIDTH / 2, H_HEIGHT = HEIGHT / 2, ASPECT_RATIO = WIDTH / HEIGHT;


// Main function
int main() {
    // Creating environment
    Object planet, sputnik, moon;
    
    planet.mass = 5.9736 * 1e4 * 6.6743;
    planet.pos = {0, 0};
    planet.vel = {0, 0};
    
    sputnik.mass = 82.6;
    sputnik.pos = {6659, 0};
    sputnik.vel = {0, 8};
    
    moon.mass = 7.32 * 1e22;
    moon.pos = {392208, 0};
    moon.vel = {0, 1};
    
    // Trajectory vector
    VertexArray linesTr(LineStrip, 1);
    linesTr[0].position = Vector2f(int(sputnik.pos.x * coeff + H_WIDTH), int(H_HEIGHT - sputnik.pos.y * coeff));
    int linesCount = 0;
    bool speedUp = false;
    
    // Creating window
    RenderWindow window(VideoMode(WIDTH, HEIGHT), "MIPH (visual)");
//    window.setFramerateLimit(100);
//    window.setVerticalSyncEnabled(true);
    
    FPS fps;
    Clock uTime, dTime;
    
    // Main cycle
    while (window.isOpen()){
        // User-input and Window events updating
        Event event;
        while (window.pollEvent(event)){
            if (event.type == Event::Closed)
                window.close();
            
            if (event.type == Event::KeyPressed)
                if (Keyboard::isKeyPressed(Keyboard::S))
                    speedUp ^= 1;
            
            // Mouse events
            if (event.type == Event::MouseButtonPressed){
                string filename = resourcePath() + "../../../screenshot.png";
                Texture texture;
                texture.create(window.getSize().x, window.getSize().y);
                texture.update(window);
                if (texture.copyToImage().saveToFile(filename)) printf("screenshot saved to %s\n", filename.c_str());
            }
        }
        
        // Environments updating
        if (uTime.getElapsedTime().asSeconds() >= (speedUp ? 0 : deltaTime)){
            long double r3 = pow(dist(moon.pos, planet.pos), 3);
            
            sputnik.a = {
                planet.mass * (planet.pos.x - sputnik.pos.x) / pow(dist(sputnik.pos, planet.pos), 3),
                planet.mass * (planet.pos.y - sputnik.pos.y) / pow(dist(sputnik.pos, planet.pos), 3)
            };

            sputnik.vel.x += sputnik.a.x * deltaTime; sputnik.vel.y += sputnik.a.y * deltaTime;
            sputnik.pos.x += sputnik.vel.x * deltaTime; sputnik.pos.y += sputnik.vel.y * deltaTime;

            moon.a = {
                planet.mass * (planet.pos.x - moon.pos.x) / r3,
                planet.mass * (planet.pos.y - moon.pos.y) / r3
            };

            moon.vel.x += moon.a.x * deltaTime; moon.vel.y += moon.a.y * deltaTime;
            moon.pos.x += moon.vel.x * deltaTime; moon.pos.y += moon.vel.y * deltaTime;

            simTime += deltaTime;
            uTime.restart();
        }

        if (dTime.getElapsedTime().asSeconds() >= 1 / tickRate){
            // Drawing
            window.clear();
            
            Vector2f newLine = Vector2f(int(sputnik.pos.x * coeff + H_WIDTH), int(H_HEIGHT - sputnik.pos.y * coeff));
            if (linesTr[linesCount].position != newLine){
                linesTr.append(newLine);
                linesTr[++linesCount].color = Color(100, 255, 100);
            }
            
            CircleShape ball(4, 4), ball2(6371 * coeff, 50), ball3(1737 * coeff, 30);
            
            ball.setPosition(sputnik.pos.x * coeff + H_WIDTH - 4, H_HEIGHT - 4 - sputnik.pos.y * coeff);
            ball.setFillColor(Color(255, 100, 100));
            
            ball2.setPosition(planet.pos.x * coeff + H_WIDTH - 6371 * coeff, H_HEIGHT - 6371 * coeff - planet.pos.y * coeff);
            ball2.setFillColor(Color(100, 150, 255));
            
            ball3.setPosition(moon.pos.x * coeff + H_WIDTH - 1737 * coeff, H_HEIGHT - 1737 * coeff - moon.pos.y * coeff);
            ball3.setFillColor(Color(200, 200, 200));
            
            window.draw(ball);
            window.draw(ball2);
            window.draw(ball3);
            window.draw(linesTr);
            
            dTime.restart();
            
            // Screen updating
            fps.update();
            window.setTitle("$~ MIPH ~fps: " + to_string(fps.getFPS()) + " ~time: " + to_string(simTime));
            window.display();
        }
    }

    return 0;
}
