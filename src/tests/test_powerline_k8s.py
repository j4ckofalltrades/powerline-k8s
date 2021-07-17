import logging

import pytest
from kubernetes import config
from powerline_k8s import k8s
from powerline_k8s.segments import SegmentColorscheme, SegmentContent, SegmentVisibility

CLUSTER_MOCK = 'minikube'
CONTEXT_MOCK = 'minikube'
NAMESPACE_MOCK = 'staging'


def build_k8s_segment(context=CONTEXT_MOCK, namespace=NAMESPACE_MOCK, hide_ns=False):
    icon_section = {
        'contents': f'{SegmentContent.K8S_ICON.value} ',
        'divider_highlight_group': SegmentColorscheme.DIVIDER_HIGHLIGHT_GROUP.value,
        'highlight_groups': [SegmentColorscheme.DEFAULT_HIGHLIGHT_GROUP.value]
    }
    context_section = {
        'contents': context,
        'divider_highlight_group': SegmentColorscheme.DIVIDER_HIGHLIGHT_GROUP.value,
        'highlight_groups': [SegmentColorscheme.CONTEXT_HIGHLIGHT_GROUP.value]
    }

    if hide_ns == True:
        return [icon_section, context_section]

    return [
        icon_section,
        context_section,
        {
            'contents': ':',
            'divider_highlight_group': SegmentColorscheme.DIVIDER_HIGHLIGHT_GROUP.value,
            'highlight_groups': [SegmentColorscheme.DEFAULT_HIGHLIGHT_GROUP.value]
        },
        {
            'contents': namespace,
            'divider_highlight_group': SegmentColorscheme.DIVIDER_HIGHLIGHT_GROUP.value,
            'highlight_groups': [SegmentColorscheme.NAMESPACE_HIGHLIGHT_GROUP.value]
        }
    ]


@pytest.fixture
def mock_pl():
    logging.basicConfig()
    return logging.getLogger()


@pytest.fixture
def mock_hide_full_segment_config(monkeypatch):
    monkeypatch.setenv(SegmentVisibility.SHOW_SEGMENT.value, "0")


@pytest.fixture
def mock_hide_namespace_section_config(monkeypatch):
    monkeypatch.setenv(SegmentVisibility.SHOW_NAMESPACE.value, "0")


@pytest.fixture
def mock_k8s_context_full(monkeypatch):
    def mock_list_contexts():
        return ([{}, {'context': {'cluster': CLUSTER_MOCK, 'namespace': NAMESPACE_MOCK}, 'name': CONTEXT_MOCK}])

    monkeypatch.setattr(config, 'list_kube_config_contexts', mock_list_contexts)


@pytest.fixture
def mock_k8s_namespace_empty(monkeypatch):
    def mock_list_contexts():
        return ([{}, {'context': {'cluster': CLUSTER_MOCK, 'namespace': ''}, 'name': CONTEXT_MOCK}])

    monkeypatch.setattr(config, 'list_kube_config_contexts', mock_list_contexts)


@pytest.fixture
def mock_no_kubeconfig(monkeypatch):
    def mock_list_contexts():
        return None

    monkeypatch.setattr(config, 'list_kube_config_contexts', mock_list_contexts)


@pytest.mark.usefixtures('mock_k8s_context_full')
def test_full_segment(mock_pl):
    assert k8s(pl=mock_pl) == build_k8s_segment()


@pytest.mark.usefixtures('mock_k8s_namespace_empty')
def test_namespace_default(mock_pl):
    assert k8s(pl=mock_pl) == build_k8s_segment(namespace='default')


@pytest.mark.usefixtures('mock_no_kubeconfig')
def test_no_kubeconfig(mock_pl):
    assert k8s(pl=mock_pl) == []


@pytest.mark.usefixtures('mock_k8s_context_full', 'mock_hide_full_segment_config')
def test_hide_full_segment_config(mock_pl):
    assert k8s(pl=mock_pl) == []


@pytest.mark.usefixtures('mock_k8s_context_full', 'mock_hide_namespace_section_config')
def test_hide_namespace_section_config(mock_pl):
    assert k8s(pl=mock_pl) == build_k8s_segment(hide_ns=True)
