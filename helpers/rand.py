import aiohttp


async def get_random_seed() -> dict:
    """从 drand 获取一个随机种子"""
    url = "https://drand.cloudflare.com/public/latest"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                return {"round": data["round"], "seed": data["randomness"]}
            else:
                raise Exception(f"Failed to fetch random seed: {response.status}")


async def _test_get_random_number():
    """测试从 drand 的种子生成随机数"""
    round = (await get_random_seed())["round"]
    print(f"Drand Round: {round}")
    seed = (await get_random_seed())["seed"]
    print(f"Random Seed: {seed}")
    import random

    random.seed(seed)
    rand_number = random.randint(1, 100)
    print(f"Random Number: {rand_number}")


async def choose_random_winners(
        participants: list[int], number_of_winners: int
) -> dict:
    """从参与者列表中随机选择获奖者"""
    rounds = (await get_random_seed())["round"]
    seed = (await get_random_seed())["seed"]
    import random

    random.seed(seed)
    winners = random.sample(participants, k=number_of_winners)
    return {"winners": winners, "round": rounds, "seed": seed}


async def get_random_tarot_card(num: int) -> dict:
    """随机抽取指定数目的塔罗牌"""
    tarot_cards = [
        # Major Arcana
        "愚者", "魔术师", "女祭司", "皇后", "皇帝", "教皇", "恋人", "战车", "力量", "隐者", "命运之轮", "正义", "倒吊人", "死神", "节制", "恶魔", "高塔", "星星", "月亮", "太阳", "审判", "世界",
        # Minor Arcana - Wands / 权杖
        "权杖首牌", "权杖二", "权杖三", "权杖四", "权杖五", "权杖六",  "权杖七",  "权杖八",  "权杖九",  "权杖十",  "权杖侍从",  "权杖骑士",  "权杖皇后",  "权杖国王",
        # Minor Arcana - Cups / 圣杯
        "圣杯首牌", "圣杯二",  "圣杯三",  "圣杯四",  "圣杯五",  "圣杯六",  "圣杯七",  "圣杯八",  "圣杯九",  "圣杯十",  "圣杯侍从",  "圣杯骑士",  "圣杯皇后",  "圣杯国王",
        # Minor Arcana - Swords / 宝剑
        "宝剑首牌", "宝剑二",  "宝剑三",  "宝剑四",  "宝剑五",  "宝剑六",  "宝剑七",  "宝剑八",  "宝剑九",  "宝剑十",  "宝剑侍从",  "宝剑骑士",  "宝剑皇后",  "宝剑国王",
        # Minor Arcana - Pentacles / 星币
        "星币首牌", "星币二", "星币三", "星币四",  "星币五",  "星币六",  "星币七",  "星币八",  "星币九",  "星币十",  "星币侍从",  "星币骑士",  "星币皇后",  "星币国王"
    ]

    rounds = (await get_random_seed())["round"]
    seed = (await get_random_seed())["seed"]
    import random

    random.seed(seed)

    # 随机选择指定数量的牌（不重复）
    selected_cards = random.sample(tarot_cards, k=min(num, len(tarot_cards)))

    # 为每张牌随机决定正位或逆位
    cards_with_position = []
    for card in selected_cards:
        position = random.choice(["正位", "逆位"])
        cards_with_position.append(f"{card}（{position}）")

    return {"cards": cards_with_position, "round": rounds, "seed": seed}


async def get_random_dice_number(dices: int, max_num: int) -> list:
    """掷骰子，返回每个骰子的点数"""
    seed = (await get_random_seed())["seed"]
    import random

    random.seed(seed)

    results = [random.randint(1, max_num) for _ in range(dices)]
    return results


if __name__ == "__main__":
    import asyncio

    asyncio.run(_test_get_random_number())
