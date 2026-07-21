// include ROS parts
#include <ros/ros.h>
#include <dynamic_reconfigure/server.h>
#include "object_detector/objectDetectorConfig.h"
#include <sensor_msgs/PointCloud2.h>
// include PCL parts
#include <pcl_conversions/pcl_conversions.h>
#include <pcl/point_types.h>
#include <pcl/filters/passthrough.h>
#include <pcl/filters/voxel_grid.h>
#include <pcl/common/common.h>
#include <pcl/search/kdtree.h>
#include "../include/object_detector/dbscan.h"
// include STL parts
#include <algorithm>
#include <vector>
// include MSG
#include <lidar_interfaces/ObjectInfo.h>

#include <cmath>
using namespace std;


// alias for point types
typedef pcl::PointXYZ PointT;       
/*  pcl point type
struct PointXYZ {
    float x;
    float y;
    float z;
    };
    */
   
// ROI parameter
double zMin, zMax, xMin, xMax, yMin, yMax;
// DBScan parameter
int minPoints;
double epsilon, minClusterSize, maxClusterSize;
// VoxelGrid parameter
float leafSize;
   
int section = 0;
   
   
   
// =====================[ ObjectInfo Messages 캐시 ]=====================
   
lidar_interfaces::ObjectInfo voxelMsg = lidar_interfaces::ObjectInfo();
   

// =====================[ ROS I/O ]=====================

// ---------------------[ ROS Subscribers ]---------------------

//  topic: "/velodyne_points"
//  type: "sensor_msgs::PointCloud2"
//  meaning: 메인 LiDAR 원본 점군을 입력받음
//  callback: mainCallback()
ros::Subscriber sub;


// ----------------------[ ROS Publishers ]----------------------

//  topic: "/roi_raw"
//  type: "sensor_msgs::PointCloud2"
//  meaning: ROI()와 ROI_LANE()에서 필터링한 ROI 점군을 발행
ros::Publisher pubROI;

//  topic: "/voxel_info"
//  type: "lidar_interfaces::ObjectInfo"
//  meaning: VoxelGrid 다운샘플링 결과를 복셀 단위 메타데이터로 발행
ros::Publisher pubVoxelInfo;








// =====================[ Callback Functions ]=====================

// dynamic_reconfigure callback.
// config에 들어온 ROI, DBSCAN, VoxelGrid 설정값을 읽는다.
// 읽어온 값을 전역 파라미터 xMin, xMax, yMin, yMax, zMin, zMax,
// minPoints, epsilon, minClusterSize, maxClusterSize, leafSize에 복사한다.
// 이후 들어오는 point cloud 처리 함수들은 갱신된 전역 파라미터를 사용한다.
void cfgCallback(object_detector::objectDetectorConfig &config, int32_t level);

// "/velodyne_points" topic callback.
// 메인 LiDAR 원본 점군을 입력받는다.
// 입력 점군을 ROI()로 필터링한 뒤 voxelGrid()로 복셀 메타데이터를 발행하고,
// 같은 ROI 점군에 대해 cluster()로 객체 단위 클러스터링을 수행한다.
// 처리 후 objectMsg와 voxelMsg를 초기화해서 다음 프레임 결과를 다시 채울 준비를 한다.
void mainCallback(const sensor_msgs::PointCloud2ConstPtr& input);




// =====================[ Processing Functions ]=====================

// sensor_msgs::PointCloud2를 pcl::PointCloud<PointT>로 변환한다.
// z, x, y 순서로 PassThrough ROI를 적용해 관심 영역의 점만 남긴다.
// section == 3이면 sectorFilterDeg()를 추가 적용해 전방 부채꼴 영역만 남긴다.
// 최종 결과를 "/roi_raw" 토픽으로 발행하고, 필터링된 점군 포인터를 반환한다.
pcl::PointCloud<PointT>::Ptr ROI(const sensor_msgs::PointCloud2ConstPtr& input);

// ROI 결과를 leafSize 기준으로 다운샘플링한다.
// 각 복셀의 중심/크기/경계를 voxelMsg에 채워 "/voxel_info"로 발행하고,
// 다운샘플된 점군 포인터를 반환한다.
pcl::PointCloud<PointT>::Ptr voxelGrid(pcl::PointCloud<PointT>::Ptr input);

// 빈 frame_id가 들어오면 RViz에서 바로 버려지므로 기본 라이다 프레임으로 보정한다.
static std_msgs::Header normalizedHeader(const std_msgs::Header& header) {
    std_msgs::Header normalized = header;
    if (normalized.frame_id.empty()) {
        normalized.frame_id = "velodyne";
    }
    return normalized;
}




// =====================[ Point Cloud Processing ]=====================

pcl::PointCloud<PointT>::Ptr ROI (const sensor_msgs::PointCloud2ConstPtr& input) {
    // ... do data processing
    pcl::PointCloud<PointT>::Ptr cloud(new pcl::PointCloud<PointT>);

    pcl::fromROSMsg(*input, *cloud); // sensor_msgs -> PointCloud 형변환

    pcl::PointCloud<PointT>::Ptr cloud_filtered(new pcl::PointCloud<PointT>);
    // std::cout << "Loaded : " << cloud->width * cloud->height << '\n';

    // 오브젝트 생성
    // Z축 ROI
    pcl::PassThrough<PointT> filter;
    filter.setInputCloud(cloud);                //입력
    filter.setFilterFieldName("z");             //적용할 좌표 축 (eg. Z축)
    filter.setFilterLimits(zMin, zMax);          //적용할 값 (최소, 최대 값)
    filter.filter(*cloud_filtered);             //필터 적용

    // X축 ROI
    filter.setInputCloud(cloud_filtered);                //입력
    filter.setFilterFieldName("x");             //적용할 좌표 축 (eg. X축)
    filter.setFilterLimits(xMin, xMax);          //적용할 값 (최소, 최대 값)
    filter.filter(*cloud_filtered);             //필터 적용

    // Y축 ROI
    filter.setInputCloud(cloud_filtered);                //입력
    filter.setFilterFieldName("y");             //적용할 좌표 축 (eg. Y축)
    filter.setFilterLimits(yMin, yMax);          //적용할 값 (최소, 최대 값)
    filter.filter(*cloud_filtered);             //필터 적용


    sensor_msgs::PointCloud2 roi_raw;
    pcl::toROSMsg(*cloud_filtered, roi_raw);
    roi_raw.header = normalizedHeader(input->header);

    pubROI.publish(roi_raw);

    return cloud_filtered;
}


pcl::PointCloud<PointT>::Ptr voxelGrid(pcl::PointCloud<PointT>::Ptr input) {
    //Voxel Grid를 이용한 DownSampling
    pcl::VoxelGrid<PointT> vg;    // VoxelGrid 선언
    pcl::PointCloud<PointT>::Ptr cloud_filtered(new pcl::PointCloud<PointT>); //Filtering 된 Data를 담을 PointCloud 선언
    voxelMsg = lidar_interfaces::ObjectInfo();
    voxelMsg.objectCounts = 0;
    std::fill(voxelMsg.centerX.begin(), voxelMsg.centerX.end(), 0.0);
    std::fill(voxelMsg.centerY.begin(), voxelMsg.centerY.end(), 0.0);
    std::fill(voxelMsg.centerZ.begin(), voxelMsg.centerZ.end(), 0.0);
    std::fill(voxelMsg.lengthX.begin(), voxelMsg.lengthX.end(), 0.0);
    std::fill(voxelMsg.lengthY.begin(), voxelMsg.lengthY.end(), 0.0);
    std::fill(voxelMsg.lengthZ.begin(), voxelMsg.lengthZ.end(), 0.0);
    std::fill(voxelMsg.minX.begin(), voxelMsg.minX.end(), 0.0);
    std::fill(voxelMsg.minY.begin(), voxelMsg.minY.end(), 0.0);
    std::fill(voxelMsg.minZ.begin(), voxelMsg.minZ.end(), 0.0);
    std::fill(voxelMsg.maxX.begin(), voxelMsg.maxX.end(), 0.0);
    std::fill(voxelMsg.maxY.begin(), voxelMsg.maxY.end(), 0.0);
    std::fill(voxelMsg.maxZ.begin(), voxelMsg.maxZ.end(), 0.0);
    std::fill(voxelMsg.pixelX.begin(), voxelMsg.pixelX.end(), 0);
    std::fill(voxelMsg.pixelY.begin(), voxelMsg.pixelY.end(), 0);

    vg.setInputCloud(input);             // Raw Data 입력
    vg.setLeafSize(leafSize, leafSize, leafSize); // 사이즈를 너무 작게 하면 샘플링 에러 발생
    vg.filter(*cloud_filtered);          // Filtering 된 Data를 cloud PointCloud에 삽입

    size_t voxel_count = cloud_filtered->points.size();
    if (voxel_count > voxelMsg.centerX.size()) {
        ROS_WARN_THROTTLE(1.0, "voxelGrid output has %zu voxels; publishing the first %zu entries only.",
                          voxel_count, voxelMsg.centerX.size());
        voxel_count = voxelMsg.centerX.size();
    }

    const double half_leaf = static_cast<double>(leafSize) * 0.5;
    for (size_t i = 0; i < voxel_count; ++i) {
        const PointT& voxel = cloud_filtered->points[i];

        voxelMsg.centerX[i] = voxel.x;
        voxelMsg.centerY[i] = voxel.y;
        voxelMsg.centerZ[i] = voxel.z;

        voxelMsg.lengthX[i] = leafSize;
        voxelMsg.lengthY[i] = leafSize;
        voxelMsg.lengthZ[i] = leafSize;

        voxelMsg.minX[i] = voxel.x - half_leaf;
        voxelMsg.minY[i] = voxel.y - half_leaf;
        voxelMsg.minZ[i] = voxel.z - half_leaf;
        voxelMsg.maxX[i] = voxel.x + half_leaf;
        voxelMsg.maxY[i] = voxel.y + half_leaf;
        voxelMsg.maxZ[i] = voxel.z + half_leaf;
    }

    voxelMsg.objectCounts = static_cast<int32_t>(voxel_count);
    pubVoxelInfo.publish(voxelMsg);

    return cloud_filtered;
}






// =====================[ Callback Implementations ]=====================

void cfgCallback(object_detector::objectDetectorConfig &config, int32_t level) {
    xMin = config.xMin;
    xMax = config.xMax;
    yMin = config.yMin;
    yMax = config.yMax;
    zMin = config.zMin;
    zMax = config.zMax;

    minPoints = config.minPoints;
    epsilon = config.epsilon;
    minClusterSize = config.minClusterSize;
    maxClusterSize = config.maxClusterSize;

    leafSize  = config.leafSize;
}


void mainCallback(const sensor_msgs::PointCloud2ConstPtr& input) {
    pcl::PointCloud<PointT>::Ptr cloudPtr;
    
    cloudPtr = ROI(input);
    voxelGrid(cloudPtr);
}







// =====================[ Main ]=====================
int main (int argc, char** argv) {
    // Initialize ROS
    ros::init (argc, argv, "object_detector");
    ros::NodeHandle nh;
   
    // rqt용 셋업
    dynamic_reconfigure::Server<object_detector::objectDetectorConfig> server;
    dynamic_reconfigure::Server<object_detector::objectDetectorConfig>::CallbackType f;
    f = boost::bind(&cfgCallback, _1, _2);
    server.setCallback(f);
   
    // Create ROS subscribers
    sub = nh.subscribe("velodyne_points", 1, mainCallback);

    // Create ROS publishers
    pubROI = nh.advertise<sensor_msgs::PointCloud2>("roi_raw", 1);
    pubVoxelInfo = nh.advertise<lidar_interfaces::ObjectInfo>("voxel_info", 1);


    
    // Spin
    ros::spin();
}
