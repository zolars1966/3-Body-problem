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
    vec pos, vel = {1., 0.}, a = {0., 0.};
    double mass = 1.;
};


double dist_S(vec v1, vec v2){
    return (v1.x - v2.x)*(v1.x - v2.x) + (v1.y - v2.y)*(v1.y - v2.y);
}


// Global varibales
double deltaTime = 0.01f, g = 9.81f;
float WIDTH = 800, HEIGHT = 800, H_WIDTH = WIDTH / 2, H_HEIGHT = HEIGHT / 2, ASPECT_RATIO = WIDTH / HEIGHT;


// Main function
int main() {
    // Creating environment
    Object planet, sputnik;
    
    planet.mass = 5;
    planet.pos = {0, 0};
    planet.vel = {0, -0.025};
    
    sputnik.mass = 1;
    sputnik.pos = {10, 0};
    sputnik.vel = {0, 2.25};
    
    // Trajectory vector
    VertexArray lines_s(LineStrip, 1);
    lines_s[0].position = Vector2f(sputnik.pos.x * 20 + H_WIDTH, H_HEIGHT - sputnik.pos.y * 20);
    int linesCount = 0;
    bool speedUp = false;
    
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
                if (Keyboard::isKeyPressed(Keyboard::S))
                    speedUp ^= 1;
                
                if (Keyboard::isKeyPressed(Keyboard::R) || Keyboard::isKeyPressed(Keyboard::D)){
                    if (Keyboard::isKeyPressed(Keyboard::D)){ cout << "Write new time period: "; cin >> deltaTime; };

                    planet.mass = 5;
                    planet.pos = {0, 0};
                    planet.vel = {0, -0.025};
                    
                    sputnik.mass = 1;
                    sputnik.pos = {10, 0};
                    sputnik.vel = {0, 2.25};
                    
                    lines_s.append(Vector2f(sputnik.pos.x * 20 + H_WIDTH, H_HEIGHT - sputnik.pos.y * 20));
                    lines_s[linesCount++].color = Color(200, 200, 200);
                    lines_s[linesCount].color = Color(200, 200, 200);
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
        
        lines_s.append(sf::Vector2f(sputnik.pos.x * 20 + H_WIDTH, H_HEIGHT - sputnik.pos.y * 20));
        lines_s[++linesCount].color = Color(100, 255, 100);
        CircleShape ball(5, 10);
        CircleShape ball2(25, 25);

        ball.setPosition(sputnik.pos.x * 20 + H_WIDTH - 5, H_HEIGHT - 5 - sputnik.pos.y * 20);
        ball.setFillColor(Color(255, 100, 100));
        
        ball2.setPosition(planet.pos.x * 20 + H_WIDTH - 25, H_HEIGHT - 25 - planet.pos.y * 20);
        ball2.setFillColor(Color(255, 100, 100));
        
        window.draw(ball);
        window.draw(ball2);
        window.draw(lines_s);

        // Environments updating
        if (dTime.getElapsedTime().asMilliseconds() >= deltaTime * (speedUp ? 100. : 1000.)){
            sputnik.a = {
                planet.mass * sputnik.mass * sputnik.pos.x / -dist_S(sputnik.pos, planet.pos),
                planet.mass * sputnik.mass * sputnik.pos.y / -dist_S(sputnik.pos, planet.pos)};

            sputnik.vel.x += sputnik.a.x * deltaTime; sputnik.vel.y += sputnik.a.y * deltaTime;
            sputnik.pos.x += sputnik.vel.x * deltaTime; sputnik.pos.y += sputnik.vel.y * deltaTime;
            
            planet.a = {
                planet.mass * sputnik.mass * planet.pos.x / -dist_S(sputnik.pos, planet.pos),
                planet.mass * sputnik.mass * planet.pos.y / -dist_S(sputnik.pos, planet.pos)};

            planet.vel.x += planet.a.x * deltaTime; planet.vel.y += planet.a.y * deltaTime;
            planet.pos.x += planet.vel.x * deltaTime; planet.pos.y += planet.vel.y * deltaTime;
                        
            dTime.restart();
        }

        // Screen updating
        fps.update();
        window.setTitle("MIPH (visual) fps: " + to_string(fps.getFPS()));
        window.display();
    }

    return 0;
}
