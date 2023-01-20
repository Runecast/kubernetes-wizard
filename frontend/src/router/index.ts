import Vue from 'vue'
import VueRouter, { RouteConfig } from 'vue-router'
import K8sWizard from '@/views/K8sWizard.vue'
import ResourceSelector from '@/views/ResourceSelector.vue';
import ModifyDataset from '@/views/ModifyDataset.vue';

Vue.use(VueRouter)

const routes: Array<RouteConfig> = [
  {
    path: '/',
    name: 'select-resource',
    component: ResourceSelector
  },
  {
    path: '/wizard',
    name: 'K8sWizard',
    component: K8sWizard
  },
  {
    path: '/modify',
    name: 'ModifyDataset',
    component: ModifyDataset
  },
  {
    path: '*',
    name: 'redirect',
    redirect: '/',
    component: ResourceSelector
  },
]

const router = new VueRouter({
  routes,
  mode: 'history'
})

export default router
