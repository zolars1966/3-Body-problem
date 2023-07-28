/*

A simple Earth gravitation simulation.
Moon and Sputnik are moving around the Earth
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
struct vec { long double x, y; };


// 2D object structure
struct Object {
    vec pos, vel = {1., 0.}, a = {0., 0.};
    double mass = 1.;
};


double dist(vec v1, vec v2){
    return sqrt((v1.x - v2.x)*(v1.x - v2.x) + (v1.y - v2.y)*(v1.y - v2.y));
}


// Global varibales
double tickRate = 60, deltaTime = 0.005f, coeff = 0.001, simTime = 0, shiftX = 0, shiftY = 0;
float WIDTH = 800, HEIGHT = 800, H_WIDTH = WIDTH / 2, H_HEIGHT = HEIGHT / 2, ASPECT_RATIO = WIDTH / HEIGHT;


Vector2f transformCoordsVec2f(vec pos){
    return Vector2f(
        static_cast<long double>((pos.x + shiftX) * coeff + H_WIDTH),
        static_cast<long double>(H_HEIGHT - (pos.y - shiftY) * coeff)
    );
}


void transformBall(vec pos, CircleShape &ball, Color color){
    ball.setPosition(
        int((pos.x + shiftX) * coeff + H_WIDTH - ball.getRadius()),
        int(H_HEIGHT - ball.getRadius() - (pos.y - shiftY) * coeff)
    );
    
    ball.setFillColor(color);
}


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
    linesTr[0].position = transformCoordsVec2f(sputnik.pos);
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
            
            if (event.type == Event::KeyPressed){
                if (Keyboard::isKeyPressed(Keyboard::R)) speedUp ^= 1;
                
                if (Keyboard::isKeyPressed(Keyboard::Q)) coeff *= 0.95;
                if (Keyboard::isKeyPressed(Keyboard::E)) coeff *= 1.05;
                
                if (Keyboard::isKeyPressed(Keyboard::W)) shiftY += 10 / coeff;
                if (Keyboard::isKeyPressed(Keyboard::S)) shiftY -= 10 / coeff;
                if (Keyboard::isKeyPressed(Keyboard::A)) shiftX += 10 / coeff;
                if (Keyboard::isKeyPressed(Keyboard::D)) shiftX -= 10 / coeff;
                
                linesTr.clear();
                linesCount = 0;
                linesTr.append(transformCoordsVec2f(sputnik.pos));
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
        
        // Environments updating
        if (uTime.getElapsedTime().asSeconds() >= (speedUp ? 0 : deltaTime)){
            long double r31 = pow(dist(moon.pos, planet.pos), 3), r32 = pow(dist(sputnik.pos, planet.pos), 3);
            
            sputnik.a = {
                planet.mass * (planet.pos.x - sputnik.pos.x) / r32,
                planet.mass * (planet.pos.y - sputnik.pos.y) / r32
            };
            sputnik.vel.x += sputnik.a.x * deltaTime;
            sputnik.vel.y += sputnik.a.y * deltaTime;
            sputnik.pos.x += sputnik.vel.x * deltaTime;
            sputnik.pos.y += sputnik.vel.y * deltaTime;

            moon.a = {
                planet.mass * (planet.pos.x - moon.pos.x) / r31,
                planet.mass * (planet.pos.y - moon.pos.y) / r31
            };
            moon.vel.x += moon.a.x * deltaTime;
            moon.vel.y += moon.a.y * deltaTime;
            moon.pos.x += moon.vel.x * deltaTime;
            moon.pos.y += moon.vel.y * deltaTime;

            simTime += deltaTime;
            uTime.restart();
        }

        if (dTime.getElapsedTime().asSeconds() >= 1 / tickRate){
            // Drawing
            window.clear();
            
            Vector2f newLine = transformCoordsVec2f(sputnik.pos);
            if (linesTr[linesCount].position != newLine){
                linesTr.append(newLine);
                linesTr[++linesCount].color = Color(100, 255, 100);
            }
            
            CircleShape ball(4, 4), ball2(6371 * coeff, 50), ball3(1737 * coeff, 30);
            
            transformBall(sputnik.pos, ball, Color(255, 100, 100));
            transformBall(planet.pos, ball2, Color(100, 150, 255));
            transformBall(moon.pos, ball3, Color(200, 200, 200));
            
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
