from maze_game import MazeGame

def main():
    # 난이도 순서대로 진행
    difficulties = ["Easy", "Medium", "Hard"]
    
    for difficulty in difficulties:
        print(f"\n{difficulty} 난이도 시작!")
        game = MazeGame(difficulty)
        game.run()
        
        # 다음 난이도로 넘어갈지 선택
        user_input = input("계속하시겠습니까? (y/n): ").lower()
        if user_input != 'y':
            break

if __name__ == "__main__":
    main()