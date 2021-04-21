## Phân loại các thuật toán object Detection
* One-stage vs Two-stage
* Region-proposal method vs proposal-free method
* Anchor-base vs anchor-free method
### One-stage vs two-stage
* One-stage
    * Các thuật toán điển hình : SSD, Yolo v2/3 , RetinaNet
    * việc gọi là one-stage vì trong việc thiết kế model hoàn toàn không có phần rút trích chọn các vùng đặc trưng như RPN của Faster-RCNN
    * Các mô hình one-stage OD coi phần việc phát hiện đối tượng (object localization) như 1 bài toán regression(với 4 tọa độ offset, ví dụ x, y , w, h) và cũng dựa trên các pre-define box gọi là anchor để làm việc này
    * Các model dạng này thường nhanh hơn tuy nhiên ***độ chính xác*** của model thường kém hơn so với two-stage object detection
    * Tuy nhiên, một số mô hình one-stage vấn tỏ ra vượt trội hơn 1 chút so với two-stage như Retina-Net với việc thiết kế mạng theo FPN (Feature Pyramid Network) và Local Loss.
* Two-stage 
    * Các thuật toán điển hình : RCNN, Fast-RCNN, Faster-RCNN, Mask-RCNN,...
    * Việc gọi là two-stage là do cách model xử lý để lấy ra được vùng có khả năng chứa vật thể từ ảnh
    * Ví dụ : Faster-RCNN :
        * stage 1: ảnh sẽ được dưa ra 1 sub-network gọi là RPN với nhiệm vụ extract các vùng trên ảnh có khả năng chứa đối tượng dựa vào các anchor
        * stage 2 : thực hiện việc phân loại đối tượng và xác định vị trí nhờ vào việc chia làm 2 nhánh tại phần cuối của mô hình (object classification & bounding box regression)
### Region-proposal method vs Proposal-free method
**Đây chỉ là một cách phân loại khác**
* Region-proposal : đề cập đến các phương pháp sử dụng 1 cơ chế để xác định các vùng có khả năng chứa đối tượng trước(region proposal), rồi sau đó tiếp tục thực hiện các bước về object classification và bounding box regression (RCNN, Fast-RCNN, Faster-RCNN,...)
* Proposal-free : các phướng pháp như SSD, Yolo v2/v3, RetinaNet,...
### Anchor-base vs Anchor-free method
* Các thuật toán kể trên đều dựa vào 1 cơ chế gọi là Anchor hay các pre-define boxes với mục đích dự đoán vị trí của các bounding box của vật thể dựa vào các anchor đó. Tuy nhiên, việc định nghĩa các anchor size + anchor ratio còn bị phụ thuộc rất nhiều về mặt dữ liệu
* Một cách tiếp cận khác là Anchor-Free, tức là không sử dụng anchor. Trong những năm gần đây thì rất nhiều bài báo về Anchor-Free ra đời và được đánh giá tốt hơn nhiều so với các phương pháp anchor-based hiện nay, cả về phần đánh giá (mAP) và performance của model (FPS & Flops). Điển hình như :
    * DenseBox
    * FCOS/FSAF
    * CornetNet
    * CenterNet(Object as Point)
    * ...
### RPN (Region Proposal Network)
* **Luồng xử lý của Faster-RCNN có thể tím gọn lại như sau**
    * Input image được đưa qua 1 backbone CNN, thu được feature map
    * Một mạng con RPN (khá đơn giản, chỉ gồm các conv layer) dùng để trích rút ra các vùng gọi là RoI(region of Interest), hay các vùng có khả năng chứa đối tiongjw từ feature map của ảnh. Input của RPN là feature map, output của RPN bao gồm 2 phần : binary object classification (để phân biệt đối tượng với background, không quan tâm đối tượng là gì) và bounding box regression(để xác định vùng ảnh có khả năng chứa đối tượng), vậy nên RPN bao gồm 2 hàm loss và hoàn toàn có thể được huấn luyện riêng so với cả model.
    * Faster-RCNN còn định nghĩa thêm khái niệm anchor, tức các pre-defined boxes đã được định nghĩa trước lúc huận luyện mô hình với mục đích như sau: thay vì mô hình phải dự đoán trực tiếp các tọa độ offset của bounding box sẽ rất khó khăn thì sẽ dự đoán gián tiếp qua các anchors
    * Sau khi đi qua RPN, ta sẽ thu được vùng RoI với kích thước khác nhau (W & H) nên sử dụng RoI Pooling (đã có từ Fast-RCNN) để thu về cùng 1 kích thước cố định
    * Thực hiện tách thành 2 nhánh ở phần cuối của model, 1 cho object classification với N + 1 (N là tổng số class, 1 là background) với bounding box regression. Vậy nên sẽ định nghĩa thêm 2 thành phần loss nữa (tương tự RPN) và loss function của Faster-RCNN sẽ gồm 4 thành phần : 2 loss của RPN và 2 loss của Fast-RCNN
* **Faster-RCNN** :
    * sử dụng 1 mạng con gọi là RPN(Region proposal Network) với mục đích trích xuất ra các vùng có khả năng chứa đối tiongjw từ ảnh (hay còn gọi là RoI) khác hoàn toàn với các xử lí của 2 mô hình anh em trước đó là RCNN và Fast-RCNN
    * RCNN : việc trích xuất các vùng region proposal được thực hiện thông qua thuật toán selective Search để trích chọn ra các ùng có khả năng chứa đối tượng (khoảng 2000 vùng). Sau đó, các vùng (ảnh) này được resize về 1 kích thước cố định và đưa qua 1 pretrained CNN model (imagenet), rồi từ đó tiến hành xác định offset và nhãn đối tượng. Tuy nhiên, việc đưa các vùng region proposal qua mạng CNN 2000 lần khiến tốc độ thực thi của model cực kì chậm
    * Fast-RCNN : bằng việc sử dụng 1 mạng pretrained CNN để thu được feature map, rồi sử dụng Selective Search lên feature map, thay vì ảnh gốc. Vậy nên tốc độ xử lý của model được cải thiện lên đáng kể vì chỉ phải đưa qua pretrained CNN model đúng 1 lần. Tuy nhiên, vì việc vấn sử dụng Selective Search nên inference time của model vẫn khá lâu (khoảng 2s/image)
    * Với Faster-RCNN, thay vì việc sử dụng Selective Search mô hình được thiết kế thêm 1 mạng con gọi là RPN để rút các vùng có khả năng chứa đối tượng của ảnh. Nhìn chung, sau khi thực hiện RPN, các bước xử lí sau tương tự Fast-RCNN nhưng nhanh hơn nhiều (vì mạng không sử dụng selective search) và được thiết kế như 1 mạng end-to-end trainable network
    * Về cơ bản, đầu tiên PRN sử dụng 1 conv layer với 512 channels, kernel_size = (3,3) lên feature map. Sau đó được chia 2 nhanh, 1 cho binary object classification , 1 cho bounding box regression. Cả 2 sử dụng 1 conv layer với kernel size = (1,1) nhưng với số channel đầu ra khác nhau
        * Binary object classification : có 2k channel output, với k là tổng số lượng anchors nhằm xác định rằng 1 anchor có khả năng chứa đối tượng hay là background(không quan tâm đối tượng gì). Thực chất, ở đây số channel có thể chuyển về chỉ còn k channel với việc sử dụng sigmoid activation.
        * Bounding box regression : có 4k channels output với 4 biểu trưng cho 4 tọa độ offset(x, y , w, h)
    * Chú ý rằng , RPN hiện tại là 1 mạng fully convolution network nên không cần kích thước đầu vao phải cố định hay ảnh dầu vào của Faster-RCNN phải cố định. Tuy nhiên, nhìn chung ta thường tiến hành resize ảnh về 1 base_width/base_height nhất định mà image ratio vẫn giữ nhiên , hoặc set 2 khoảng giá trị min/max như repo của [TF object detection API](https://github.com/tensorflow/models/blob/master/research/object_detection/samples/configs/faster_rcnn_inception_v2_coco.config#L13-L14) 
    * Vì đầu vào kích thước ảnh không cố định nên kích thước đầu ra của RPN cũng không cố định. Ví dụ với 1 ảnh đầu vào với kích thước WxHx3, với down sampling = 16 thì RPN_classify và RPN_bounding_box lần lượt là 18*(W / 16 )*( H / 16) và 36*(W / 16)*(H / 16)
### Anchors 
* anchor hay còn gọi là các pre-defined boxes, được định nghĩa trước lúc khi huấn luyện mô hình. Anchor trong Faster-RCNN được định nghĩa với 9 anchors ứng với mỗi điểm pixel trên feature map. Chú ý rằng, việc tính toán tổng số lượng anchor là dựa trên kích thước của feature map. Ví dụ : feature map thu được sau khi đưa qua backbone CNN có kích thước là WxHxC (với C là số channel của feature map) thì tổng số lượng anchor là WxHx9 (9 là số lượng anchor ứng với 1 điểm pixle của feature map). Tuy nhiên, kích thước và ratio của anchor thì đều phải tham chiếu ngược lại kích thước của ảnh gốc ban đầu.
* Các anchor được tạo ra là ứng với từng điểm pixel trên feature map và thông thường được định nghĩa với 3 anchor size và 3 anchor ratio khác nhau .
* Các anchor này được assign là possive/nagative (object / background) dựa vào diện tích trung lặp hay IoU overlap với ground truth bounding box theo rule sau:
    * Các anchor có tỉ lệ IoU lớn nhất với ground truth box sẽ được coi là positive 
    * Các anchor có tỉ lệ IoU >= 0.7 sẽ được coi là positive 
    * Các anchor có tỉ lệ IoU < 0.3 sẽ được coi là negative (background)
    * Các anchor nằm trong khoảng 0.3 <= x < 0.7 sẽ được coi là neural (trung tính ) là sẽ không được sử dụng trong quá trình huấn luyện mô hình
* Việc tạo ra các anchor nhằm mục đích như sau :
    * Dựa vào IoU để phân biệt các positive và negative anchors 
    * Dựa vào vị trí của các pre-defined anchor và các ground-truth bounding box (thông qua tỉ lệ IoU), dự đoán vị trí của các region proposal đầu ra
    * Dễ thấy số lượng negative anchor là lớn hơn rất nhiều so với positive anchor, nên trong paper có đề cập tới 1 hướng xử lý để thực hiện training mô hình gọi là **image centric**. Trong deep learning, các bạn đã nghe tới khá niệm batch_size là số sample sẽ được xử lý trong 1 step. Trong Faster-RCNN 1 batch_size sẽ chỉ ứng với 1 ảnh. Tuy nhiên, dữ liệu chính cần sử dụng ở đây là chính các pre-define anchor đã được định nghĩa. Vì tổng số lượng anchor là rất nhiều nên với 1 ảnh sẽ chỉ thực hiện lấy k = 256 anchor là chia đề 2 phần (128 positive anchors + 128 negative anchors)
    * Tuy nhiên,  không phải lúc nào cũng có đủ số lượng positive anchor trong 1 ảnh. vậy nên, hướng xử lý trong paper là nếu không đủ positive anchor thì thay thế bằng ác negative anchor khác
    * Với các vùng RoI thu được sau RPN sẽ bị overlap lên nhau khá nhiều nên cần 1 cơ chế để filter-out các vùng đó. 1 phướng pháp được đề xuất là NMS (Non-maximum suppresstion). Ý tướng của NMS vô cùng đơn giản:
        * Ta có 1 tập các vùng RoI thu được gọi là R kèm các confidence score S tương ứng và 1 giá trị overlap threshold N. Đồng thời, khởi tạo 1 list rỗng D
        * Chọn vùng RoI với confidence score cao nhất và xóa khỏi R, thêm vào D
        * So sánh vùng RoI mới được thêm vào D với tất cả các vùng RoI đang có trong R qua metric IoU. Nếu giá trị threshold lớn hơn giá trị overlap threshold N được khởi tạo ban đầu thì loại bỏ các vùng RoI đó ra khởi R
        * Tiếp tục chọn vùng RoI có confidence score cao nhất hiện tại có trong R và thêm vào D
        * So sánh giá trị IoU của vùng vừa được thêm vào D với các vùng còn lại trong R, nếu > overlap threshold thì loại khỏi R 
        * Tiếp tục thực hiện như vậy đến khi không còn phần tử nòa trong R
        * Tuy nhiên, thuật toán NMS ban đầu cũng có những nhược điểm nhất định. Ví dụ như nếu ngưỡng overlap threshold là 0.5. giả dụ có những vùng RoI có overlap IoU = 0.51 nhưng có confidence score rất cao nhưng lại bị loại ra khỏi tập R. Ngược lại, có nhũng vùng RoI thỏa mãn overlap IoU < 0.5 nhưng confidence score không cao, nên không bị loại khỏi R và mô hình chung làm giảm "chất lượng" của model xuống
    * Tuy nhiên, thuật toán NMS ban đầu cũng có những nhược điểm nhất định. Ví dụ như nếu ngưỡng overlap threshold là 0.5. Giả dụ có những vùng RoI có overlap IoU = 0.51 nhưng có confidence score rất cao nhưng lại bị loại khỏi tập R. Ngược laijm có những vùng RoI thỏa mãn overlap IoU < 0.5 nhưng confidence score không cao, nên không bị loại khỏi R và mô hình chung làm giảm "chất lượng" của model xuống.
    * Một thuật toán được đề xuất là Soft-NMS giúp cải thiện được việc dùng 1 giá trị overlap threshold fix cừng từ ban đầu. Ý tưởng vô cùng đơn giản : Thay vì loại bỏ ác vùng RoI có overlap threshold cao mà confidence score lớn, ta thực hiện giảm confidence xuống tỉ lệ với giá trị IoU thu được
### ROI Pooling 
* RoI Pooling đã được đề cập trong mô hình Fast-RCNN trước đó với mục đích cố định kích thước đầu ra của feature map sau khi thực hiện RoI Pooling. Việc thực hiện RoI Pooling là bắt buộc vì phần cuối của mạng gồm 2 nhánh Fully connected layer yêu cầu input size phải cố định
* Hãy tưởng tượng ảnh minh họa 4 con mèo dưới gồm các vùng ROI màu đỉ thực tế số lượng vùng là lớn hơn rất nhiều và overlap nhau khá nhiều
* Như đã nói ở phần trên, tọa độ offset của vùng RoI được xác định tham chiếu theo kích thước ảnh input nên ta cũng có thể trích rút các vùng RoI trên chính feature map. Có thể dễ thấy rằng kích thước của feature map nhỏ hơn 32 lần kích thước của ảnh đầu vào (từ 512 -> 16) nên tọa độ offset của các vùng RoI xét trên feature map (x,y,w,h) cũng sẽ bị giảm xuống 32 lần! Điều này là quan trọng và cần chú ý.