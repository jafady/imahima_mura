import axios from 'axios'
import Store from '../store';

declare module '@vue/runtime-core' {
  export interface ComponentCustomProperties {
    $http: typeof axios
    $store: typeof Store;
    $validate: (data: Record<string, unknown>, rule: Record<string, unknown>) => boolean
  }
}