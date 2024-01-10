# -*- coding: utf-8 -*-

import os
from enum import Enum

from kubernetes import config
from powerline.segments import Segment, with_docstring


class SegmentColorscheme(Enum):
    """Colorscheme configuration for the segment sections."""

    DIVIDER_HIGHLIGHT_GROUP = "k8s:divider"
    """Sections divider's background and foreground colors."""

    DEFAULT_HIGHLIGHT_GROUP = "k8s"
    """Icon and divider's background and foreground colors."""

    CONTEXT_HIGHLIGHT_GROUP = "k8s_context"
    """k8s context section's background and foreground colors."""

    NAMESPACE_HIGHLIGHT_GROUP = "k8s_namespace"
    """k8s namespace section's background and foreground colors."""


class SegmentContent(Enum):
    """Default values for segment's sections."""

    CTX_DEFAULT = 'N/A'
    """Default k8s context name."""

    NS_DEFAULT = 'default'
    """Default k8s namespace name."""

    K8S_ICON = u'\U00002638'
    """Default icon for segment."""


class SegmentVisibility(Enum):
    """Environment variable names for toggling segment visibility."""

    SHOW_SEGMENT = "POWERLINE_K8S_SHOW"
    """Toggle entire segment visibility by setting the value to either 1 (show) or 0 (hide)."""

    SHOW_NAMESPACE = "POWERLINE_K8S_SHOW_NS"
    """Toggle namespace visibility in segment by setting the value to either 1 (show) or 0 (hide)."""


class KubernetesSegment(Segment):
    """Constructs the segment's sections with the configured colorscheme and visibility options applied."""

    @staticmethod
    def kube_ctx_info(pl):
        """Resolves the current active Kubernetes context (and namespace) from `$KUBECONFIG`."""
        try:
            current_context = config.list_kube_config_contexts()[1]
            return current_context.get('name', SegmentContent.CTX_DEFAULT.value) or SegmentContent.CTX_DEFAULT.value, \
                   current_context.get('context', {}).get('namespace', SegmentContent.NS_DEFAULT.value) or SegmentContent.NS_DEFAULT.value
        except Exception as e:
            pl.error(e)

    def __call__(self, pl):
        pl.debug('Running powerline-k8s...')

        sections = []

        ctx_info = self.kube_ctx_info(pl)
        if ctx_info is None:
            return sections

        show_segment = os.getenv(SegmentVisibility.SHOW_SEGMENT.value)
        if show_segment is None:
            pass
        elif int(show_segment) == 0:
            return sections

        sections.append({
            'contents': f'{SegmentContent.K8S_ICON.value} ',
            'highlight_groups': [SegmentColorscheme.DEFAULT_HIGHLIGHT_GROUP.value],
            'divider_highlight_group': SegmentColorscheme.DIVIDER_HIGHLIGHT_GROUP.value,
        })

        context = ctx_info[0]
        sections.append({
            'contents': context,
            'highlight_groups': [SegmentColorscheme.CONTEXT_HIGHLIGHT_GROUP.value],
            'divider_highlight_group': SegmentColorscheme.DIVIDER_HIGHLIGHT_GROUP.value,
        })

        show_namespace = os.getenv(SegmentVisibility.SHOW_NAMESPACE.value)
        if show_namespace is None:
            pass
        elif int(show_namespace) == 0:
            return sections

        separator = ':'
        sections.append({
            'contents': separator,
            'highlight_groups': [SegmentColorscheme.DEFAULT_HIGHLIGHT_GROUP.value],
            'divider_highlight_group': SegmentColorscheme.DIVIDER_HIGHLIGHT_GROUP.value,
        })

        namespace = ctx_info[1]
        sections.append({
            'contents': namespace,
            'highlight_groups': [SegmentColorscheme.NAMESPACE_HIGHLIGHT_GROUP.value],
            'divider_highlight_group': SegmentColorscheme.DIVIDER_HIGHLIGHT_GROUP.value,
        })

        return sections


k8s = with_docstring(KubernetesSegment(), """Return the current Kubernetes context and namespace.

It will show the current context and namespace from `$KUBECONFIG`.

Divider highlight group used: ``k8s:divider``.

Highlight groups used: ``k8s``, ``k8s_context``, ``k8s_namespace``.
""")
"""Custom segment entry point."""
