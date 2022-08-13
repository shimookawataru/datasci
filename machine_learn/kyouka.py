import gym
from gym import wrappers
import numpy as np
import time

def _bins(clip_min, clip_max, num):
    return np.linspace(clip_min, clip_max, num + 1)[1:-1]


# 状態を離散化して表にする関数
def digitize_state(observation):
    cart_pos, cart_v, pole_angle, pole_v = observation
    digitized = [
        np.digitize(cart_pos, bins=_bins(-2.4, 2.4, num_dizitized)),
        np.digitize(cart_v, bins=_bins(-3.0, 3.0, num_dizitized)),
        np.digitize(pole_angle, bins=_bins(-0.5, 0.5, num_dizitized)),
        np.digitize(pole_v, bins=_bins(-2.0, 2.0, num_dizitized))
    ]
    return sum([x * (num_dizitized**i) for i, x in enumerate(digitized)])
# Q関数表をもとに，行動を選択する関数
# force_best=Trueの場合は，常に最適な行動を取る（Greedy法）
# そうでなければ ε-Greedy法
def get_action(next_state, episode, force_best=False):
    epsilon = 0.5 * (1 / (episode + 1))
    if force_best or epsilon <= np.random.uniform(0, 1):
        next_action = np.argmax(q_table[next_state])
    else:
        next_action = np.random.choice([0, 1])
    return next_action

# Q関数の更新
def update_Qtable(q_table, state, action, reward, next_state, next_action):
    gamma = 0.99
    alpha = 0.5
    q_table[state, action] = (1 - alpha) * q_table[state, action] +\
            alpha * (reward + gamma * q_table[next_state, next_action])

    return q_table

env = gym.make('CartPole-v0')

max_number_of_steps = 200  #1試行のstep数
num_consecutive_iterations = 100  #学習完了評価に使用する平均試行回数
num_episodes = 2000  #総試行回数

goal_average_reward = 195  #この報酬を超えると学習終了（中心への制御なし）

# 状態を6分割^（4変数）に離散化してQ関数（表）を作成
num_dizitized = 6  #分割数
q_table = np.random.uniform(low=-1, high=1, size=(num_dizitized**4, env.action_space.n))
total_reward_vec = np.zeros(num_consecutive_iterations)  #各試行の報酬を格納
islearned = 0  #学習が終わったフラグ
isrender = 0  #描画フラグ

for episode in range(num_episodes):  #試行数分繰り返す
    # 環境の初期化
    observation = env.reset()
    state = digitize_state(observation)
    action = np.argmax(q_table[state])
    episode_reward = 0

    for t in range(max_number_of_steps):  #1試行のループ
        if islearned == 1:  #学習終了したらcartPoleを描画する
            env.render()
            print (observation[0])  #カートのx位置を出力

        # 行動a_tの実行により、s_{t+1}, r_{t}などを計算する
        observation, reward, done, info = env.step(action)

        # 報酬を設定し与える
        if done:
            if t < 195:
                reward = -200  #こけたら罰則
            else:
                reward = 1  #立ったまま終了時は罰則はなし
        else:
            reward = 1  #各ステップで立ってたら報酬追加

        episode_reward += reward  #報酬を追加

        # 離散状態s_{t+1}を求める
        next_state = digitize_state(observation)  #t+1での観測状態を、離散値に変換

        #　SARSAによるQ関数表の更新
        next_action = get_action(next_state, episode)    # 次の行動a_{t+1}を求める
        q_table = update_Qtable(q_table, state, action, reward, next_state, next_action)

        # 次の行動と状態に更新
        action = next_action    # a_{t+1}
        state = next_state      # s_{t+1}

        # 終了時の処理
        if done:
            print('%d Episode finished after %f time steps / mean %f' %
                  (episode, t + 1, total_reward_vec.mean()))
            total_reward_vec = np.hstack((total_reward_vec[1:],
                                          episode_reward))  #報酬を記録
            break

    if (total_reward_vec.mean() >= goal_average_reward):
        print('Episode %d train agent successfuly!' % episode)
        islearned = 1
        if isrender == 0:
            isrender = 1
