from keras.models import load_model
from keras.preprocessing.image import img_to_array
import numpy as np
from  PIL import Image
import pickle


class M2model:

    def __init__(self,model_path = "models/MovileNetV2_8_pred.h5"):
        self.model = load_model(model_path)


        with open("models/pca_zero_ver3_30.pkl", "rb") as f:
            self.pca_zero = pickle.load(f)

        with open("models/pca_cora_ver3_30.pkl", "rb") as f:
            self.pca_cora = pickle.load(f)

        with open("models/pca_ocha_ver3_30.pkl", "rb") as f:
            self.pca_ocha = pickle.load(f)

        with open("models/pca_irohasu_ver3_40.pkl", "rb") as f:
            self.pca_irohasu = pickle.load(f)

        with open("models/pca_orange_ver3_30.pkl", "rb") as f:
            self.pca_orange = pickle.load(f)


    def Pca_process(self, n_class, img):

        if n_class == 1:
            reshape = img.reshape(1, -1)
            pca_data = self.pca_zero.transform(reshape)
            pca_redata = self.pca_zero.inverse_transform(pca_data)
            diff = np.sum(np.abs(reshape - pca_redata))
            if diff > 9000:
                return 0
            else:
                return n_class

        if n_class == 2:
            reshape = img.reshape(1, -1)
            pca_data = self.pca_cora.transform(reshape)
            pca_redata = self.pca_cora.inverse_transform(pca_data)
            diff = np.sum(np.abs(reshape - pca_redata))
            if diff > 9000:
                return 0
            else:
                return n_class

        if n_class == 3:
            reshape = img.reshape(1, -1)
            pca_data = self.pca_ocha.transform(reshape)
            pca_redata = self.pca_ocha.inverse_transform(pca_data)
            diff = np.sum(np.abs(reshape - pca_redata))
            if diff > 9000:
                return 0
            else:
                return n_class

        if n_class == 4:
            reshape = img.reshape(1, -1)
            pca_data = self.pca_irohasu.transform(reshape)
            pca_redata = self.pca_irohasu.inverse_transform(pca_data)
            diff = np.sum(np.abs(reshape - pca_redata))
            if diff > 9000:
                return 0
            else:
                return n_class

        if n_class == 5:
            reshape = img.reshape(1, -1)
            pca_data = self.pca_orange.transform(reshape)
            pca_redata = self.pca_orange.inverse_transform(pca_data)
            diff = np.sum(np.abs(reshape - pca_redata))
            if diff > 9000:
                return 0
            else:
                return n_class


    def predict(self, path="./0_0.png"):
        img = Image.open(path)
        img = img.convert("RGB")
        img = img.resize((224, 224))
        img_array = img_to_array(img)
        img_array = img_array.astype('float32')/255.0
        img_array = img_array.reshape((1,224,224,3))

        pred = self.model.predict(img_array)
        n_class = np.argmax(pred)
        n_class += 1

        ans = self.Pca_process(n_class, img_array)

        return ans
