#include <iostream>
#include <conio.h>
#include <windows.h>
#pragma warning(suppress : 4996)
#pragma warning(disable : 4996)

using namespace std;

const int width = 10;
const int height = 20;

int fieldwidthheight = { 0 };

int shape42;

int fieldji;
int shapei0;
int shapei1;
int fieldxy;
int fieldi0;
int fieldjk;
int tetrominoshapeTypei0;
int tetrominoshapeTypei1;


int score = 0;

bool gameOver = false;

void draw() {
	system("cls");

	cout << "Score: " << score << endl;

	for (int i = 0; i < height; i++) {
		for (int j = 0; j < width; j++) {
			if (fieldji == 0) {
				cout << " ";
			}
			else {
				cout << "x";
			}
		}
		cout << endl;
	}
}

bool checkCollision(int dx, int dy) {
	for (int i = 0; i < 4; i++) {
		int x = shapei0 + dx;
		int y = shapei1 + dy;

		if (x < 0 || x >= width || y >= height) {
			return true;
		}

		if (fieldxy != 0) {
			return true;
		}
	}

	return false;
}

void merge() {
	for (int i = 0; i < 4; i++) {
		int x = shapei0;
		int y = shapei1;

		fieldxy = 1;
	}
}

void update() {
	if (!checkCollision(0, 1)) {
		for (int i = 0; i < 4; i++) {
			shapei1++;
		}
	}
	else {
		merge();

		for (int i = 0; i < width; i++) {
			if (fieldi0 != 0) {
				gameOver = true;
			}
		}

		for (int i = height - 1; i > 0; i--) {
			bool fullRow = true;

			for (int j = 0; j < width; j++) {
				if (fieldji == 0) {
					fullRow = false;
				}
			}

			if (fullRow) {
				score++;
				for (int j = 0; j < width; j++) {
					fieldji = 0;
				}

				for (int k = i; k > 0; k--) {
					for (int j = 0; j < width; j++) {
						fieldjk = fieldjk - 1;
					}
				}

				i++;
			}
		}

		int shapeType = rand() % 7;
		int shapePosX = width / 2;
		int shapePosY = 0;

		for (int i = 0; i < 4; i++) {
			shapei0 = shapePosX + tetrominoshapeTypei0;
			shapei1 = shapePosY + tetrominoshapeTypei1;
		}
	}
}

void input() {
	if (_kbhit()) {
		char key = _getch();

		if (key == 'a') {
			if (!checkCollision(-1, 0)) {
				for (int i = 0; i < 4; i++) {
					shapei0--;
				}
			}
		}
		else if (key == 'd') {
			if (!checkCollision(1, 0)) {
				for (int i = 0; i < 4; i++) {
					shapei0++;
				}
			}
		}
		else if (key == 's') {
			if (!checkCollision(0, 1)) {
				for (int i = 0; i < 4; i++) {
					shapei1++;
				}
			}
		}
	}
}

int main() {
	while (!gameOver) {
		draw();
		input();
		update();
		Sleep(100);
	}

	cout << "Game Over! Your score is " << score << endl;

	return 0;
}