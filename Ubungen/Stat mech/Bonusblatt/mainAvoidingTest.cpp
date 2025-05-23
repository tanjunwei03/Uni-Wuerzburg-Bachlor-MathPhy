#include <cstdio>
#include <vector>
#include <random>
#include <math.h>
#include <fstream>
#include <iostream>
#include <set>

inline int sqDist(std::pair<int,int> coord){
	return coord.first*coord.first + coord.second*coord.second;
}

class RandomWalk {
	public:
		int N; //Length
		std::vector<std::pair<int,int>> coords; //list of positions
		std::pair<int,int> currentPos;
		std::set<std::pair<int,int>> visited;

		//random device
		static std::random_device rd;
		/* This may not be a random seed!
		 * https://en.cppreference.com/w/cpp/numeric/random/random_device
		 * On my computer, it generated the same numbers at every run
		 * Maybe it works better on yours lmao
		 */
		static std::mt19937 gen; //static so different class instances generate different numbers
        static std::discrete_distribution<> dist;

		RandomWalk(int Np){
            this -> N = Np;
		}

		int generateWalk(){
		//reset variables
		currentPos = std::make_pair(0,0);
		coords = std::vector<std::pair<int,int>>();
		visited = std::set<std::pair<int,int>>();

		coords.push_back(currentPos);
		visited.insert(currentPos);

		for (int i = 0; i < N; ++i){
			int dir = dist(gen); //0 for right, 1 for up, 2 for left, 3 for down
			switch (dir){
				case 0:
					currentPos.first++;
					break;
				case 1:
					currentPos.second++;
					break;
				case 2:
					currentPos.first--;
					break;
				case 3:
					currentPos.second--;
			}
			coords.push_back(currentPos);
			if (visited.count(currentPos)) return 1;
		}
		return 0;
		}

		int generateAvoidingWalk(){
		while (true){
			int x = generateWalk();
			if (not x) return 0;
		}
		}
};

//Initialize static random members
std::random_device RandomWalk::rd;
std::mt19937 RandomWalk::gen(rd());
std::discrete_distribution<> RandomWalk::dist({1,1,1,1});


int main(){
	int numExperiments = 1000000;
	int L = 40; //length of a single walk
	std::vector<std::vector<int>> distances(numExperiments, std::vector<int>(L+1,0));
	RandomWalk rw = RandomWalk(L);
	//here we also export the first 20 walks, 20 is hardcoded
	std::ofstream outfile;
	outfile.open("trajectoriesAvoiding.csv");
	for (int exp = 0; exp < numExperiments; ++exp){
		rw.generateAvoidingWalk();
		for (int i = 1; i <= L; ++i) distances[exp][i] = sqDist(rw.coords[i]);
		if (exp < 20) for (int i = 1; i <= L; ++i) outfile << rw.coords[i].first << "," << rw.coords[i].second << "\n"; //here is the exporting of the trajectory
	}
	outfile.close();
}
