#include <iostream>
#include <sw/redis++/redis++.h>

using namespace sw::redis;


#include <Windows.h>
class CTimer
{
public:
    CTimer() : m_nTimeStampMicro(0.0) {
        QueryPerformanceFrequency(&m_nFrequency);
    }
    void SetMark() { m_nTimeStampMicro = GetCurTimeMicro(); }
    std::uint64_t GetElapsedTimeMicro()
    {
        std::uint64_t nElapsedTimeMicro = GetCurTimeMicro() - m_nTimeStampMicro;
        return nElapsedTimeMicro;
    }
    std::uint64_t GetElapsedTimeMili()
    {
        return GetElapsedTimeMicro() / 1000.;
    }
    

protected:
    std::uint64_t GetCurTimeMicro()
    {
        LARGE_INTEGER nTime;
        QueryPerformanceCounter(&nTime);
        nTime.QuadPart *= 1000000;
        nTime.QuadPart /= m_nFrequency.QuadPart;
        return nTime.QuadPart;
    };

    LARGE_INTEGER m_nFrequency;
    std::uint64_t m_nTimeStampMicro;
};





int main() {
    const std::uint32_t nEntsToadSize = 5000;

    try {
        CTimer cMyTimer;
        cMyTimer.SetMark();
        std::uint64_t nEllapsedMili = cMyTimer.GetElapsedTimeMili();

#if 0
        ConnectionOptions connection_options;
        connection_options.host = "simulhackathonredis2.redis.cache.windows.net";
        connection_options.port = 6379; //6380 for secure port
        connection_options.password = "PRIMARY KEY";
        auto redis = Redis(connection_options);
#elif 1
        ConnectionOptions connection_options;
        connection_options.host = "docksegenredis.redis.cache.windows.net";
        connection_options.port = 6379; //6380 for secure port
        connection_options.password = "PRIMARY KEY";
        auto redis = Redis(connection_options);
#else 
        auto redis = Redis("tcp://127.0.0.1:6379");
        nEllapsedMili = cMyTimer.GetElapsedTimeMili();
        std::cout << "Redis('tcp://127.0.0.1:6379'');" << nEllapsedMili << "\n";
#endif
        // HSET entity:1 name Marina lat 34.1 lon 33.2

#if 1
        cMyTimer.SetMark();
        auto pipeW = redis.pipeline(false);
        for (std::uint32_t nEntIdx = 0U; nEntIdx < nEntsToadSize; nEntIdx++)
        {
            char szEntId[30];
            char szEntName[30];
            char szEntLatVal[30];
            char szEntLonVal[30];
            char szEntTime[30];

            std::sprintf(szEntId, "entity:%d", nEntIdx);
            std::sprintf(szEntName, "Marina%d", nEntIdx);
            std::sprintf(szEntLatVal, "22.%d", nEntIdx);
            std::sprintf(szEntLonVal, "23.%d", nEntIdx);
            std::uint64_t nEllapsedMili = cMyTimer.GetElapsedTimeMili();
            std::sprintf(szEntTime, "%d", (int)nEllapsedMili);

            pipeW.hset(szEntId, "Name", szEntName);
            pipeW.hset(szEntId, "lat", szEntLatVal);
            pipeW.hset(szEntId, "lon", szEntLonVal);
            pipeW.hset(szEntId, "Time", szEntTime);
        }
        pipeW.exec();
        nEllapsedMili = cMyTimer.GetElapsedTimeMili();
        std::cout << nEntsToadSize << " setters with pipe " << nEllapsedMili << " mili" << "\n";
#endif

#if 0
        cMyTimer.SetMark();
        for (std::uint32_t nEntIdx = 0U; nEntIdx < nEntsToadSize; nEntIdx++)
        {
            char szEntId[30];
            std::sprintf(szEntId, "entity:%d", nEntIdx);
            std::unordered_map<std::string, std::string> hash;
            redis.hgetall(szEntId, std::inserter(hash, hash.end()));
        }

        nEllapsedMili = cMyTimer.GetElapsedTimeMili();
        std::cout << nEntsToadSize << " getters " << nEllapsedMili << " mili" << "\n";
#endif
        while (1)
        {

            cMyTimer.SetMark();
            auto pipeR = redis.pipeline(false);
            /*std::uint64_t nEllapsedMili = cMyTimer.GetElapsedTimeMili();
            char szEntTime[30];
            std::sprintf(szEntTime, "%d", (int)nEllapsedMili);
            pipeR.hset("entity:1", "Time", szEntTime);*/

            for (std::uint32_t nEntIdx = 0U; nEntIdx < nEntsToadSize; nEntIdx++)
            {
                char szEntId[30];
                std::sprintf(szEntId, "entity:%d", nEntIdx);
                pipeR.hgetall(szEntId);
            }
            auto replies = pipeR.exec();
            for (std::uint32_t nEntIdx = 0U; nEntIdx < nEntsToadSize; nEntIdx++)
            {
                std::vector<std::string> lrange_cmd_result;
                replies.get(nEntIdx, back_inserter(lrange_cmd_result));
            }

            nEllapsedMili = cMyTimer.GetElapsedTimeMili();
            std::cout << nEntsToadSize << " getters with pipe " << nEllapsedMili << " mili" << "\n";

            std::vector<std::string> lrange_cmd_result;
            replies.get(1 , back_inserter(lrange_cmd_result));
            
            for (std::uint32_t nStrIdx = 2U; nStrIdx < lrange_cmd_result.size(); nStrIdx++)
            {
                std::cout << lrange_cmd_result[nStrIdx] << " ";
            }
            std::cout << "\n";
        }
        
    }
    catch (const Error& e) {
        std::cerr << "Error:" << e.what() << "\n";
    }

  return 0;
}


