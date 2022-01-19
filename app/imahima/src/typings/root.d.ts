import axios from 'axios'
import Store from '../store';

declare module '@vue/runtime-core' {
  export interface ComponentCustomProperties {
    $http: typeof axios
    $store: typeof Store;
    $validate: (data: object, rule: object) => boolean
  }
}