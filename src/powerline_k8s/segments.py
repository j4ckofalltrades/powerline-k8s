import os

from kubernetes import config
from powerline.segments import Segment, with_docstring

CTX_DEFAULT = 'N/A'
NS_DEFAULT = 'default'
K8S_ICON = u'\U00002638'


class KubernetesSegment(Segment):
    """
    Attempt to parse the current context and namespace from the kube-config file.
    """

    @staticmethod
    def kube_ctx_info(pl):
        try:
            config.load_kube_config()
            current_context = config.list_kube_config_contexts()[1]
            return current_context['name'] or CTX_DEFAULT, current_context['context']['namespace'] or NS_DEFAULT
        except Exception as e:
            pl.error(e)

    def __call__(self, pl):
        pl.debug('Running powerline-k8s')

        sections = []

        ctx_info = self.kube_ctx_info(pl)
        if ctx_info is None:
            return sections

        show_segment = os.getenv("POWERLINE_K8S_SHOW")
        if show_segment is None:
            pass
        elif int(show_segment) == 0:
            return sections

        sections.append({
            'contents': f'{K8S_ICON} ',
            'highlight_groups': ['k8s'],
            'divider_highlight_group': 'k8s:divider',
        })

        context = ctx_info[0]
        sections.append({
            'contents': context,
            'highlight_groups': ['k8s_context'],
            'divider_highlight_group': 'k8s:divider',
        })

        show_namespace = os.getenv("POWERLINE_K8S_SHOW_NS")
        if show_namespace is None:
            pass
        elif int(show_namespace) == 0:
            return sections

        separator = ':'
        sections.append({
            'contents': separator,
            'highlight_groups': ['k8s'],
            'divider_highlight_group': 'k8s:divider',
        })

        namespace = ctx_info[1]
        sections.append({
            'contents': namespace,
            'highlight_groups': ['k8s_namespace'],
            'divider_highlight_group': 'k8s:divider',
        })

        return sections


k8s = with_docstring(KubernetesSegment(), '''Return the current Kubernetes context and namespace.

It will show the current context and namespace from the kube-config file.

Divider highlight group used: ``k8s:divider``.

Highlight groups used: ``k8s``, ``k8s_context``, ``k8s_namespace``.
''')
