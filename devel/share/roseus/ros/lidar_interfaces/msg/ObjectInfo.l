;; Auto-generated. Do not edit!


(when (boundp 'lidar_interfaces::ObjectInfo)
  (if (not (find-package "LIDAR_INTERFACES"))
    (make-package "LIDAR_INTERFACES"))
  (shadow 'ObjectInfo (find-package "LIDAR_INTERFACES")))
(unless (find-package "LIDAR_INTERFACES::OBJECTINFO")
  (make-package "LIDAR_INTERFACES::OBJECTINFO"))

(in-package "ROS")
;;//! \htmlinclude ObjectInfo.msg.html


(defclass lidar_interfaces::ObjectInfo
  :super ros::object
  :slots (_objectCounts _centerX _centerY _centerZ _lengthX _lengthY _lengthZ _minX _minY _minZ _maxX _maxY _maxZ _pixelX _pixelY ))

(defmethod lidar_interfaces::ObjectInfo
  (:init
   (&key
    ((:objectCounts __objectCounts) 0)
    ((:centerX __centerX) (make-array 100 :initial-element 0.0 :element-type :float))
    ((:centerY __centerY) (make-array 100 :initial-element 0.0 :element-type :float))
    ((:centerZ __centerZ) (make-array 100 :initial-element 0.0 :element-type :float))
    ((:lengthX __lengthX) (make-array 100 :initial-element 0.0 :element-type :float))
    ((:lengthY __lengthY) (make-array 100 :initial-element 0.0 :element-type :float))
    ((:lengthZ __lengthZ) (make-array 100 :initial-element 0.0 :element-type :float))
    ((:minX __minX) (make-array 100 :initial-element 0.0 :element-type :float))
    ((:minY __minY) (make-array 100 :initial-element 0.0 :element-type :float))
    ((:minZ __minZ) (make-array 100 :initial-element 0.0 :element-type :float))
    ((:maxX __maxX) (make-array 100 :initial-element 0.0 :element-type :float))
    ((:maxY __maxY) (make-array 100 :initial-element 0.0 :element-type :float))
    ((:maxZ __maxZ) (make-array 100 :initial-element 0.0 :element-type :float))
    ((:pixelX __pixelX) (make-array 100 :initial-element 0 :element-type :integer))
    ((:pixelY __pixelY) (make-array 100 :initial-element 0 :element-type :integer))
    )
   (send-super :init)
   (setq _objectCounts (round __objectCounts))
   (setq _centerX __centerX)
   (setq _centerY __centerY)
   (setq _centerZ __centerZ)
   (setq _lengthX __lengthX)
   (setq _lengthY __lengthY)
   (setq _lengthZ __lengthZ)
   (setq _minX __minX)
   (setq _minY __minY)
   (setq _minZ __minZ)
   (setq _maxX __maxX)
   (setq _maxY __maxY)
   (setq _maxZ __maxZ)
   (setq _pixelX __pixelX)
   (setq _pixelY __pixelY)
   self)
  (:objectCounts
   (&optional __objectCounts)
   (if __objectCounts (setq _objectCounts __objectCounts)) _objectCounts)
  (:centerX
   (&optional __centerX)
   (if __centerX (setq _centerX __centerX)) _centerX)
  (:centerY
   (&optional __centerY)
   (if __centerY (setq _centerY __centerY)) _centerY)
  (:centerZ
   (&optional __centerZ)
   (if __centerZ (setq _centerZ __centerZ)) _centerZ)
  (:lengthX
   (&optional __lengthX)
   (if __lengthX (setq _lengthX __lengthX)) _lengthX)
  (:lengthY
   (&optional __lengthY)
   (if __lengthY (setq _lengthY __lengthY)) _lengthY)
  (:lengthZ
   (&optional __lengthZ)
   (if __lengthZ (setq _lengthZ __lengthZ)) _lengthZ)
  (:minX
   (&optional __minX)
   (if __minX (setq _minX __minX)) _minX)
  (:minY
   (&optional __minY)
   (if __minY (setq _minY __minY)) _minY)
  (:minZ
   (&optional __minZ)
   (if __minZ (setq _minZ __minZ)) _minZ)
  (:maxX
   (&optional __maxX)
   (if __maxX (setq _maxX __maxX)) _maxX)
  (:maxY
   (&optional __maxY)
   (if __maxY (setq _maxY __maxY)) _maxY)
  (:maxZ
   (&optional __maxZ)
   (if __maxZ (setq _maxZ __maxZ)) _maxZ)
  (:pixelX
   (&optional __pixelX)
   (if __pixelX (setq _pixelX __pixelX)) _pixelX)
  (:pixelY
   (&optional __pixelY)
   (if __pixelY (setq _pixelY __pixelY)) _pixelY)
  (:serialization-length
   ()
   (+
    ;; int32 _objectCounts
    4
    ;; float64[100] _centerX
    (* 8    100)
    ;; float64[100] _centerY
    (* 8    100)
    ;; float64[100] _centerZ
    (* 8    100)
    ;; float64[100] _lengthX
    (* 8    100)
    ;; float64[100] _lengthY
    (* 8    100)
    ;; float64[100] _lengthZ
    (* 8    100)
    ;; float64[100] _minX
    (* 8    100)
    ;; float64[100] _minY
    (* 8    100)
    ;; float64[100] _minZ
    (* 8    100)
    ;; float64[100] _maxX
    (* 8    100)
    ;; float64[100] _maxY
    (* 8    100)
    ;; float64[100] _maxZ
    (* 8    100)
    ;; int64[100] _pixelX
    (* 8    100)
    ;; int64[100] _pixelY
    (* 8    100)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; int32 _objectCounts
       (write-long _objectCounts s)
     ;; float64[100] _centerX
     (dotimes (i 100)
       (sys::poke (elt _centerX i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;; float64[100] _centerY
     (dotimes (i 100)
       (sys::poke (elt _centerY i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;; float64[100] _centerZ
     (dotimes (i 100)
       (sys::poke (elt _centerZ i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;; float64[100] _lengthX
     (dotimes (i 100)
       (sys::poke (elt _lengthX i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;; float64[100] _lengthY
     (dotimes (i 100)
       (sys::poke (elt _lengthY i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;; float64[100] _lengthZ
     (dotimes (i 100)
       (sys::poke (elt _lengthZ i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;; float64[100] _minX
     (dotimes (i 100)
       (sys::poke (elt _minX i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;; float64[100] _minY
     (dotimes (i 100)
       (sys::poke (elt _minY i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;; float64[100] _minZ
     (dotimes (i 100)
       (sys::poke (elt _minZ i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;; float64[100] _maxX
     (dotimes (i 100)
       (sys::poke (elt _maxX i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;; float64[100] _maxY
     (dotimes (i 100)
       (sys::poke (elt _maxY i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;; float64[100] _maxZ
     (dotimes (i 100)
       (sys::poke (elt _maxZ i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;; int64[100] _pixelX
     (dotimes (i 100)
#+(or :alpha :irix6 :x86_64)
       (progn (sys::poke (elt _pixelX i) (send s :buffer) (send s :count) :long) (incf (stream-count s) 8))
#-(or :alpha :irix6 :x86_64)
       (cond ((and (class (elt _pixelX i)) (= (length ((elt _pixelX i) . bv)) 2)) ;; bignum
              (write-long (ash (elt ((elt _pixelX i) . bv) 0) 0) s)
              (write-long (ash (elt ((elt _pixelX i) . bv) 1) -1) s))
             ((and (class (elt _pixelX i)) (= (length ((elt _pixelX i) . bv)) 1)) ;; big1
              (write-long (elt ((elt _pixelX i) . bv) 0) s)
              (write-long (if (>= (elt _pixelX i) 0) 0 #xffffffff) s))
             (t                                         ;; integer
              (write-long (elt _pixelX i) s)(write-long (if (>= (elt _pixelX i) 0) 0 #xffffffff) s)))
       )
     ;; int64[100] _pixelY
     (dotimes (i 100)
#+(or :alpha :irix6 :x86_64)
       (progn (sys::poke (elt _pixelY i) (send s :buffer) (send s :count) :long) (incf (stream-count s) 8))
#-(or :alpha :irix6 :x86_64)
       (cond ((and (class (elt _pixelY i)) (= (length ((elt _pixelY i) . bv)) 2)) ;; bignum
              (write-long (ash (elt ((elt _pixelY i) . bv) 0) 0) s)
              (write-long (ash (elt ((elt _pixelY i) . bv) 1) -1) s))
             ((and (class (elt _pixelY i)) (= (length ((elt _pixelY i) . bv)) 1)) ;; big1
              (write-long (elt ((elt _pixelY i) . bv) 0) s)
              (write-long (if (>= (elt _pixelY i) 0) 0 #xffffffff) s))
             (t                                         ;; integer
              (write-long (elt _pixelY i) s)(write-long (if (>= (elt _pixelY i) 0) 0 #xffffffff) s)))
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; int32 _objectCounts
     (setq _objectCounts (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; float64[100] _centerX
   (dotimes (i (length _centerX))
     (setf (elt _centerX i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     )
   ;; float64[100] _centerY
   (dotimes (i (length _centerY))
     (setf (elt _centerY i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     )
   ;; float64[100] _centerZ
   (dotimes (i (length _centerZ))
     (setf (elt _centerZ i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     )
   ;; float64[100] _lengthX
   (dotimes (i (length _lengthX))
     (setf (elt _lengthX i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     )
   ;; float64[100] _lengthY
   (dotimes (i (length _lengthY))
     (setf (elt _lengthY i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     )
   ;; float64[100] _lengthZ
   (dotimes (i (length _lengthZ))
     (setf (elt _lengthZ i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     )
   ;; float64[100] _minX
   (dotimes (i (length _minX))
     (setf (elt _minX i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     )
   ;; float64[100] _minY
   (dotimes (i (length _minY))
     (setf (elt _minY i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     )
   ;; float64[100] _minZ
   (dotimes (i (length _minZ))
     (setf (elt _minZ i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     )
   ;; float64[100] _maxX
   (dotimes (i (length _maxX))
     (setf (elt _maxX i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     )
   ;; float64[100] _maxY
   (dotimes (i (length _maxY))
     (setf (elt _maxY i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     )
   ;; float64[100] _maxZ
   (dotimes (i (length _maxZ))
     (setf (elt _maxZ i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     )
   ;; int64[100] _pixelX
   (dotimes (i (length _pixelX))
#+(or :alpha :irix6 :x86_64)
      (setf (elt _pixelX i) (prog1 (sys::peek buf ptr- :long) (incf ptr- 8)))
#-(or :alpha :irix6 :x86_64)
      (setf (elt _pixelX i) (let ((b0 (prog1 (sys::peek buf ptr- :integer) (incf ptr- 4)))
                  (b1 (prog1 (sys::peek buf ptr- :integer) (incf ptr- 4))))
              (cond ((= b1 -1) b0)
                     ((and (= b1  0)
                           (<= lisp::most-negative-fixnum b0 lisp::most-positive-fixnum))
                      b0)
                    ((= b1  0) (make-instance bignum :size 1 :bv (integer-vector b0)))
                    (t (make-instance bignum :size 2 :bv (integer-vector b0 (ash b1 1)))))))
     )
   ;; int64[100] _pixelY
   (dotimes (i (length _pixelY))
#+(or :alpha :irix6 :x86_64)
      (setf (elt _pixelY i) (prog1 (sys::peek buf ptr- :long) (incf ptr- 8)))
#-(or :alpha :irix6 :x86_64)
      (setf (elt _pixelY i) (let ((b0 (prog1 (sys::peek buf ptr- :integer) (incf ptr- 4)))
                  (b1 (prog1 (sys::peek buf ptr- :integer) (incf ptr- 4))))
              (cond ((= b1 -1) b0)
                     ((and (= b1  0)
                           (<= lisp::most-negative-fixnum b0 lisp::most-positive-fixnum))
                      b0)
                    ((= b1  0) (make-instance bignum :size 1 :bv (integer-vector b0)))
                    (t (make-instance bignum :size 2 :bv (integer-vector b0 (ash b1 1)))))))
     )
   ;;
   self)
  )

(setf (get lidar_interfaces::ObjectInfo :md5sum-) "85c75bf95c45558608b5f8ca10538e49")
(setf (get lidar_interfaces::ObjectInfo :datatype-) "lidar_interfaces/ObjectInfo")
(setf (get lidar_interfaces::ObjectInfo :definition-)
      "int32 objectCounts
float64[100] centerX
float64[100] centerY
float64[100] centerZ
float64[100] lengthX
float64[100] lengthY
float64[100] lengthZ
float64[100] minX
float64[100] minY
float64[100] minZ
float64[100] maxX
float64[100] maxY
float64[100] maxZ
int64[100] pixelX
int64[100] pixelY

")



(provide :lidar_interfaces/ObjectInfo "85c75bf95c45558608b5f8ca10538e49")


