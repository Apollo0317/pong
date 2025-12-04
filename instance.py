from pong.core import SceneManager

sm = None


def get_sm():
    """获取 SceneManager 单例"""
    global sm
    if sm is None:
        sm = SceneManager()
    return sm


def set_sm(scene_manager):
    """设置 SceneManager 单例（从 main.py 调用）"""
    global sm
    sm = scene_manager
