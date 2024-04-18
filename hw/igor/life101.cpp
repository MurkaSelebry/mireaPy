// This is a personal academic project. Dear PVS-Studio, please check it.

// PVS-Studio Static Code Analyzer for C, C++, C#, and Java: https://pvs-studio.com
#include <iostream>
#include <vector>
#include <cstdlib>
#include <ctime> 
#include <map> 
#include <windows.h> 
using namespace std;
struct axis {
	int x, y;
	axis() { x = y = 0; }
	axis(int x, int y) :x(x), y(y) {}//конструктор для упрощения инициализации структуры 
	//P.S. позже я узнал о новой упрощенной системе иницализации в C++, но исправлять целый код считаю не целесообразным из-за такой мелочи
};
/// <summary>
/// Функция для установки цвета вывода в консоль
/// В данном случае она нужна для красивой визуализации жизни
/// </summary>
/// <param name="text">Цвет символов</param>
/// <param name="background">Задний фон символов</param>
void SetColor(int text = 0, int background = 0)
{
	HANDLE hStdOut = GetStdHandle(STD_OUTPUT_HANDLE);
	SetConsoleTextAttribute(hStdOut, (WORD)((background << 4) | text));
}


/// <summary>
/// Класс Поле
/// Это именно то место, где живут хищники и травоядные
/// </summary>
class field {
private:
	axis size;
	char** f;//сама карта
	double count_grass, grass_recovery;
public:
	map <pair<int, int>, double> m;
	field(axis size, double count_grass, double grass_recovery) :
		size(size), count_grass(count_grass), grass_recovery(grass_recovery)
	{

		f = new char* [size.x + 2];
		for (int i = 0; i < size.x + 2; i++) f[i] = new char[size.y + 2];
		for (int i = 1; i < size.x + 1; i++)
			for (int j = 1; j < size.y + 1; j++)
				f[i][j] = ' ';
		for (int i = 0; i < size.y + 2; i++) {
			f[0][i] = 'X';
			f[size.x + 1][i] = 'X';
		}
		for (int i = 1; i < size.x + 1; i++) {
			f[i][0] = 'X';
			f[i][size.y + 1] = 'X';
		}
		generate_grass();//генерация травы на карте
	}
	void print_field() {//печать поля со всеми его жителями, включая траву
		SetColor(15, 0);
		for (int i = 0; i < size.x + 2; i++) {
			for (int j = 0; j < size.y + 2; j++) {
				if (f[i][j] == 'g') SetColor(2, 0);
				if (f[i][j] == 'P') SetColor(4, 0);
				if (f[i][j] == 'H') SetColor(11, 0);
				cout << f[i][j];
				SetColor(15, 0);
			}
			cout << '\n';
		}
	}
	axis get_size() {//возврат размера поля
		return size;
	}
	void set_mark(axis pos, char mark) {//установка марки (значка) жителя, у каждого он свой
		f[pos.x][pos.y] = mark;
	}
	void clear(axis p) {//очищение поля и проверка его на наличие травы, чтобы потом можно было применить восстановление
		if (f[p.x][p.y] == 'g') m[{p.x, p.y}] = 0;
		f[p.x][p.y] = ' ';
	}
	char get_data(axis p) {//получение информации о данной ячейке
		return f[p.x][p.y];
	}
	void generate_grass() {//функция для рандомной генерации травы
		for (int i = 0; i < count_grass * size.x * size.y; i++) {
			int x = 1 + rand() % size.x;
			int y = 1 + rand() % size.y;
				while (f[x][y] != ' ') {
					x = 1 + rand() % size.x;
					y = 1 + rand() % size.y;
				}
			f[x][y] = 'g';
			m[{x, y}] = 1;
		}
	}
	void recover_grass() {//функция восстановления травы
		for (auto it : m) {
			if (f[it.first.first][it.first.second] != 'g') {
				m[{ it.first.first, it.first.second }] += grass_recovery;
				if (it.second >= 1 && f[it.first.first][it.first.second] == ' ') f[it.first.first][it.first.second] = 'g';
			}
		}
	}
};
/// <summary>
/// Класс животное - базовый класс для Хищников и Травоядных
/// </summary>
class animal {
private:
	axis pos;
protected:
	int age, min_age, max_age, month = 0;
	double count_food, need_food;
	char mark, mark_opponent;
	void set_pos(field& f) {
		f.set_mark(axis(pos.x, pos.y), mark);
	}
public:
	bool alive = true;//статус alive говорит о том, живо ли животное
	animal() {}
	/// <summary>
	/// Конкструктор с параметрами для того, чтобы инициализировать поля класса
	/// </summary>
	/// <param name="f">ссылка на поле, чтобы работать с определенным объектом</param>
	/// <param name="count_food">Количество еды, на данный момент доступное животному</param>
	/// <param name="need_food">Количество нужной еды для проживания</param>
	/// <param name="age">Возраст животного</param>
	/// <param name="min_age">Минимальный возраст животного</param>
	/// <param name="max_age">Максимальный возраст животного</param>
	/// <param name="position">Позиция животного</param>
	/// Последние три параметра заданы по умолчанию и нет надобности в их передаче в аргументах функции
	animal(field& f, double count_food, double need_food, int age, int min_age = 0, int max_age = 12, axis position = { 0,0 }) :
		age(age), min_age(min_age), max_age(max_age), count_food(count_food), need_food(need_food), pos(position)
	{
		if (position.x == 0 && position.y == 0) {
			pos.x = 1 + rand() % f.get_size().x;
			pos.y = 1 + rand() % f.get_size().y;
			if (f.get_data(axis(pos.x, pos.y)) != ' ') {
				while (f.get_data(axis(pos.x, pos.y)) != ' ') {
					pos.x = 1 + rand() % f.get_size().x;
					pos.y = 1 + rand() % f.get_size().y;
				}
			}
		}
	}

/// <summary>
/// Аналог конкструктора, только вызывается с помощью метода init с параметрами для того, чтобы инициализировать поля класса
/// </summary>
/// <param name="f">ссылка на поле, чтобы работать с определенным объектом</param>
/// <param name="count_food">Количество еды, на данный момент доступное животному</param>
/// <param name="need_food">Количество нужной еды для проживания</param>
/// <param name="age">Возраст животного</param>
/// <param name="min_age">Минимальный возраст животного</param>
/// <param name="max_age">Максимальный возраст животного</param>
/// <param name="position">Позиция животного</param>
/// Последние три параметра заданы по умолчанию и нет надобности в их передаче в аргументах функции
	void init(field& f, double count_food, double need_food, int age, int min_age = 0, int max_age = 12, axis position = { 0,0 }) {
		this->age = age;
		this->min_age = min_age;
		this->max_age = max_age;
		this->count_food = count_food;
		this->need_food = need_food;
		pos = position;
		if (position.x == 0 && position.y == 0) {
			pos.x = 1 + rand() % f.get_size().x;
			pos.y = 1 + rand() % f.get_size().y;
				while (f.get_data(axis(pos.x, pos.y)) != ' ') {
					pos.x = 1 + rand() % f.get_size().x;
					pos.y = 1 + rand() % f.get_size().y;
				}
		}
	}
	/// <summary>
	/// АТ
	/// </summary>
	/// <param name="f"></param>
	void step(field& f) {
		if (f.get_data(get_pos()) != mark) { alive = false; return; }
		bool chec_around = true;
		for (int i = get_pos().x - 1; i <= get_pos().x + 1; i++)
			for (int j = get_pos().y - 1; j <= get_pos().y + 1; j++) {
				if (i == get_pos().x && j == get_pos().y)  
				{
					cout << "dsfds"; continue;
				}
				if (!(f.get_data(axis(i, j)) == 'g' || f.get_data(axis(i, j)) == ' ')) return;
			}
		f.clear(axis(pos.x, pos.y));
		month++;
		int x = pos.x;
		int y = pos.y;
		pos.x += rand() % 3 - 1;
		pos.y += rand() % 3 - 1;
			while (pos.x<1 || pos.x>f.get_size().x || pos.y<1 || pos.y>f.get_size().y || f.get_data(axis(pos.x, pos.y)) == mark_opponent || f.get_data(axis(pos.x, pos.y)) == mark) {
				pos.x = x;
				pos.x += rand() % 3 - 1;
				pos.y = y;
				pos.y += rand() % 3 - 1;
			}
		set_pos(f);
		if (month == 12) {
			age++; month = 0;
		}
		count_food -= 1;
	}
	axis get_pos() {
		return pos;
	}
	virtual void eat(field& f) {}
	void death_from_cataclysm(field& f, double chance) {
		double rand_death = 0.01 * (rand() % 101);;
		if (rand_death <= chance) f.clear(get_pos());
		if (f.get_data(get_pos()) != mark) alive = false;
	}
};
class predator :public animal {
public:
	predator() { }

	predator(field& f, double count_food, double need_food, int age, int min_age = 0, int max_age = 12, axis position = { 0,0 }) :
		animal(f, count_food, need_food, age, min_age, max_age, position) {
		mark = 'P';
		mark_opponent = 'H';
		set_pos(f);
	}
	void eat(field& f) {
		for (int i = get_pos().x - 1; i <= get_pos().x + 1; i++)
			for (int j = get_pos().y - 1; j <= get_pos().y + 1; j++)
				if (f.get_data(axis(i, j)) == mark_opponent) {
					f.clear(axis(i, j));
					count_food += 25;
				}
	}
	void init(field& f, double count_food, double need_food, int age, int min_age = 0, int max_age = 12, axis position = { 0,0 }) {
		animal::init(f, count_food, need_food, age, min_age, max_age, position);
		mark = 'P';
		mark_opponent = 'H';
		set_pos(f);
	}

	void death(field& f) {
		double rand_death = (rand() % 101);
		
		if ((100 - count_food) / need_food >= rand_death) f.clear(get_pos());
		if (age >= max_age) f.clear(get_pos());
		if (f.get_data(get_pos()) != mark) alive = false;
	}
	void add_food(double f) {
		count_food += f;
	}
};
class herbivore :public animal {
public:
	herbivore() {}
	herbivore(field& f, double count_food, double need_food, int age, int min_age = 0, int max_age = 12, axis position = { 0,0 }) :
		animal(f, count_food, need_food, age, min_age, max_age, position) {
		mark = 'H';
		mark_opponent = 'g';
		set_pos(f);
	}
	void init(field& f, double count_food, double need_food, int age, int min_age = 0, int max_age = 12, axis position = { 0,0 }) {
		animal::init(f, count_food, need_food, age, min_age, max_age, position);
		mark = 'H';
		mark_opponent = 'g';
		set_pos(f);
	}
	void eat(field& f) {
		for (int i = get_pos().x - 1; i <= get_pos().x + 1; i++)
			for (int j = get_pos().y - 1; j <= get_pos().y + 1; j++)
				if (f.get_data(axis(i, j)) == mark_opponent) {
					f.clear(axis(i, j));
					count_food += 10;
					f.m[{i, j}] = 0;
				}
	}
	void death(field& f, predator* arr, int size) {
		double rand_death =   (rand() % 101);
		cout << "fds "<< rand_death <<"\n";
		cout << "fdsss "<< (100 - count_food) / need_food <<"\n";
		if ((100 - count_food) / need_food >= rand_death) f.clear(get_pos());
		if (age == max_age) {
			f.clear(get_pos());
			for (int i = 0; i < size; i++) {
				arr[i].add_food(10);
			}
		}
		if (f.get_data(get_pos()) != mark) alive = false;
	}

};
template<typename T>
void input(T& n) {
	if (cin >> n); else { cout << "Вы ввели не тот тип данных!"; exit(-1); }
}
void non_gui(double p_c, double h_c, double p_c_s, double h_c_s) {
	cout << "Осталось:\n Хищников: " << p_c << " \nТравоядных: " << h_c;
	cout << "\nУмерло:\n Хищников: " << p_c_s - p_c << " \nТравоядных: " << h_c_s - h_c;
}
void gui(field& f, double p_c, double h_c, double p_c_s, double h_c_s) {
	cout << "Желаете ли вы просмотреть взаимодействие животных в графическом режиме: \n"
		<< "1.Да\n"
		<< "0.Нет\n";
	cout << "Ваш ответ: ";
	int c;
	input(c);
	cin.ignore();
	switch (c) {
	case 1:
		f.print_field();
		break;
	case 0:
		system("cls");
		non_gui(p_c, h_c, p_c_s, h_c_s);
		break;
	default:
		cout << "Такого случая нет( Проверьте правильность введенных данных и перезапустите программу)";
		exit(-1);
		break;
	}
}

int main() {
	srand(time(NULL));
	setlocale(LC_ALL, "rus");
	cout << "Введите размер поля: ";
	int x, y;
	input(x);
	input(y);
	cout << "Введите содержание травы (пример: 0.1 (10%)): ";
	double count_grass, grass_r;
	input(count_grass);
	cout << "Введите скорость восстановления травы за год: ";
	input(grass_r);
	field f(axis(x, y), count_grass, grass_r);
	double cataclysm_chance;
	cout << "Введите вероятность катаклизма: ";
	input(cataclysm_chance);
	int p_c_s, h_c_s;
	cout << "Введите количество хищников: ";
	input(p_c_s);
	cout << "Введите количество травоядных: ";
	input(h_c_s);
	herbivore* h = new herbivore[h_c_s];
	predator* p = new predator[p_c_s];
	for (int i = 0; i < p_c_s; i++) {
		cout << "Введите информацию для хищника " << i + 1 << " : ";
		double count_food, need_food;
		cout << "Введите количество еды, доступное изначально:";
		input(count_food);
		cout << "Введите количество еды, нужное для жизни:";
		input(need_food);
		cout << "Введите возраст хищника:";
		int age, min_age, max_age;
		input(age);
		cout << "Введите минимальный возраст хищника:";
		input(min_age);
		cout << "Введите максимальный возраст хищника:";
		input(max_age);
		p[i].init(f, count_food, need_food, age, min_age, max_age);
	}
	for (int i = 0; i < h_c_s; i++) {
		cout << "Введите информацию для травоядного" << i + 1 << " : ";
		double count_food, need_food;
		cout << "Введите количество еды, доступное изначально:";
		input(count_food);
		cout << "Введите количество еды, нужное для жизни:";
		input(need_food);
		cout << "Введите возраст хищника:";
		int age, min_age, max_age;
		input(age);
		cout << "Введите минимальный возраст хищника:";
		input(min_age);
		cout << "Введите максимальный возраст хищника:";
		input(max_age);
		h[i].init(f, count_food, need_food, age, min_age, max_age);
	}

	int p_c = 0, h_c = 0;
	cout << "Введите количество лет эмуляции: \n";
	int year;
	input(year);
	f.print_field();
	for (int j = 1; j < year; j++) {
		for (int k = 1; k < 12; k++) {
			p_c = 0;
			h_c = 0;
			for (int i = 0; i < p_c_s; i++) {
				if (p[i].alive) {
					p[i].eat(f);
					//p[i].step(f);
					//p[i].death(f);
					//if (j % 12 == 0) p[i].death_from_cataclysm(f, cataclysm_chance);
					if (p[i].alive) p_c++;
					//f.print_field();
				}
			}
			for (int i = 0; i < h_c_s; i++) {
				if (h[i].alive) {
					h[i].eat(f);
					//h[i].step(f);
					//h[i].death(f, p, 100);
					//if (j % 12 == 0) h[i].death_from_cataclysm(f, cataclysm_chance);
					if (h[i].alive) h_c++;
				}
			}
		}
		gui(f, p_c, h_c, p_c_s, h_c_s);
		f.recover_grass();
		system("pause");
		system("cls");
	}
	f.print_field();
	non_gui(p_c, h_c, p_c_s, h_c_s);


}