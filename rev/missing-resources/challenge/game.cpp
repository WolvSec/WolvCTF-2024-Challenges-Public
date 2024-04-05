#include <cmath>
#define SDL_MAIN_HANDLED
#include <SDL.h>
#include <SDL_events.h>
#include <SDL_ttf.h>
#include "flag.h"
#include "obfuscate.h"
#include <string>

void SDL_Fail() {
    SDL_LogError(SDL_LOG_CATEGORY_CUSTOM, "Error %s", SDL_GetError());
    exit(1);
}

int main()
{
    if (SDL_Init(SDL_INIT_VIDEO)) {
        SDL_Fail();
    }
    if (TTF_Init()) {
        SDL_Fail();
    }

    auto win = SDL_CreateWindow("Window", SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED, 430, 200, SDL_WINDOW_RESIZABLE);
    if (!win) {
        SDL_Fail();
    }

    auto renderer = SDL_CreateRenderer(win, -1, SDL_RENDERER_ACCELERATED);

    SDL_ShowWindow(win);

    // load the font
    TTF_Font* font = TTF_OpenFont("Inter-VariableFont.ttf", 24);
    if (!font) {
        SDL_Fail();
    }


    // render it to a surface
    SDL_Surface* surfaceMessage = TTF_RenderText_Solid(font, AY_OBFUSCATE(FLAG), {255,255,255});

    // make a Texture

    SDL_Texture* messageTex = SDL_CreateTextureFromSurface(renderer, surfaceMessage);

    SDL_Rect text_rect{
            .x = 0,
            .y = 0
    };
    SDL_QueryTexture(messageTex, NULL, NULL, &text_rect.w, &text_rect.h);

    bool app_quit = false;

    SDL_Event event;
    while (!app_quit) {
        while (SDL_PollEvent(&event)) {
            if (event.type == SDL_QUIT)
                app_quit = true;
            break;
        }

        auto time = SDL_GetTicks() / 1000.f;
        auto red = (std::sin(time) + 1) / 2.0 * 255;
        auto green = (std::sin(time / 2) + 1) / 2.0 * 255;
        auto blue = (std::sin(time) * 2 + 1) / 2.0 * 255;

        SDL_SetRenderDrawColor(renderer, red, green, blue, SDL_ALPHA_OPAQUE);
        SDL_RenderClear(renderer);

        SDL_RenderCopy(renderer, messageTex, NULL, &text_rect);
        SDL_RenderPresent(renderer);
    }

    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(win);
    SDL_Quit();

    return 0;
}
