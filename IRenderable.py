from abc import ABC, abstractmethod


class IRenderable(ABC):
    # @abstractmethod
    def render(self, screen, render_cfg=None, *args, **kwargs):
        pass
