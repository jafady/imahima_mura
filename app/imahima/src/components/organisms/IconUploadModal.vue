<template>
    <div class="container IUM_container">
        <label type="button" class="mypage_icon" :class="statusCss" for="file_upload" data-bs-toggle="modal" data-bs-target="#icon_upload">
            <input type="file" id="file_upload" @change="onImageUploaded" style="display: none;">
            <img id="cropped_image" :src="croppedFile" class="cropped_image" />
        </label>
        <!-- Modal -->
        <teleport to="body">
            <div class="modal fade" id="icon_upload" aria-hidden="true">
                <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable">
                    <div class="modal-content">
                        <div class="modal-body upload_body">
                            <div class="cropper_body">
                                <img id="cropping-image" :src="uploadingFile"/>
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn_cancel IUM_btn" data-bs-dismiss="modal">閉じる</button>
                            <button type="button" class="btn btn_primary_normal IUM_btn" data-bs-dismiss="modal" @click="confirmCroppingImage">保存</button>
                        </div>
                    </div>
                </div>
            </div>
        </teleport>
    </div>
</template>

<style lang="scss">
.mypage_icon{
    height: 100px;
    width: 100px;
    border-radius: 50%;
    background-position: center;
    margin: 0 auto;
    border: none;

    .cropped_image{
        width: 90px;
        height: 90px;
        margin-top: 5px;
        background-color: white;
        border-radius: 50%;
    }
}

.cropper-container{
    margin: 0 auto;
}
.cropper-view-box,
.cropper-face {
  border-radius: 50%;
  cursor: grab;
  outline: initial;
}
.cropper-face:active {
  cursor: grabbing;
}

.upload_body {
    width: 350px; 
    height: 350px;
    margin: 0 auto;

    .cropper_body {
        width: 300px; 
        height: 300px;
        margin: 0 auto;
    }
}

.IUM_btn {
    width: 70px;
    height: 40px;
}

</style>

<script lang="ts">
import { defineComponent } from 'vue'
import Cropper from "cropperjs";
import CONST from '../const'
export type DataType = {
    cropper: any,
    zoomRangeValue: number,
    uploadingFile: string | ArrayBuffer | null,
    croppedFile: string | ArrayBuffer | null,
    userStatus: string,
}

export default defineComponent({
    name: "IconUploadModal",
    components: {
    },
    data(): DataType {
        return{
            cropper: null,
            zoomRangeValue: 0,
            uploadingFile: null,
            croppedFile: require("../../assets/img/default_icon.png"),
            userStatus: "icon_bg_hima",
        }
    },
    computed: {
        statusCss(): string{
            return "icon_bg_" + this.$store.state.userStatus
        }
    },
    mounted : function():void{
        if(this.$store.state.userIcon){
            this.croppedFile = this.$store.state.userIcon;
        }else{
            this.$store.dispatch("getUserInfo").then(()=>{
                if(this.$store.state.userIcon){
                    this.croppedFile = this.$store.state.userIcon;
                }
            });
        }
    },
    methods: {
        onImageUploaded(e:any):void {
            // event(=e)から画像データを取得する
            const image = e.target.files[0];
            if(image){
                this.createImage(image);
            }
            
        },
        createImage(image:any):void {
            const reader = new FileReader();
            // imageをreaderにDataURLとしてattachする
            reader.readAsDataURL(image);
            // readAdDataURLが完了したあと実行される処理
            reader.onload = () => {
                this.uploadingFile = reader.result;
            }
            reader.onloadend = () => {
                this.makeCropper();
            }
        },
        makeCropper():void{
            if(this.cropper){
                this.cropper.destroy();
            }
            const croppingImage: HTMLImageElement = document.getElementById("cropping-image") as HTMLImageElement;

            this.cropper = new Cropper(croppingImage, {
                aspectRatio: 1,
                dragMode: "move",
                guides: false,
                center: true,
                restore: false,
                minContainerWidth: 300,
                minContainerHeight: 300,
            });
        },
        getRoundedCanvas(sourceCanvas: HTMLCanvasElement):HTMLCanvasElement {
            let canvas: HTMLCanvasElement = document.createElement("canvas");
            if (canvas !== undefined) {
                let context = canvas.getContext("2d");
                let width = sourceCanvas.width;
                let height = sourceCanvas.height;

                canvas.width = width;
                canvas.height = height;

                if (context !== null) {
                    context.imageSmoothingEnabled = true;
                    context.drawImage(sourceCanvas, 0, 0, width, height);
                    context.globalCompositeOperation = "destination-in";
                    context.beginPath();
                    context.arc(
                        width / 2,
                        height / 2,
                        Math.min(width, height) / 2,
                        0,
                        2 * Math.PI,
                        true
                    );
                    context.fill();
                }
            }
            return canvas;
        },
        confirmCroppingImage():void {
            // 「Cropper」型に一致しているかどうかを確認する。
            if (this.cropper instanceof Cropper) {
                let croppedCanvas = this.cropper.getCroppedCanvas({
                    width: 200,
                    height: 200,
                });
                let roundedCanvas = this.getRoundedCanvas(croppedCanvas);

                this.croppedFile = roundedCanvas.toDataURL();

                // 保存処理
                this.saveIcon();
            }
        },
        saveIcon():void {
            if(!this.croppedFile){
                return
            }
            const saveData:Record<string, unknown> = {};
            // 保存用に接頭辞を外す
            let data:any = this.croppedFile;
            data = data.replace(CONST.BASE64.header, '');

            saveData["icon"] = data;
            
            this.saveUserSetting(saveData);
        },
        saveUserSetting(data:any):void{
            this.$http.put("/api/user_setting/" + this.$store.state.userId + "/",data);
        }
    }
})



</script>


