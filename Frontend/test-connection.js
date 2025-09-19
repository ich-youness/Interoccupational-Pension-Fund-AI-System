// Simple test script to verify frontend-backend connection
// Run this with: node test-connection.js

const testConnection = async () => {
  try {
    console.log('Testing connection to CIMR-OS Backend...');
    
    // Test health endpoint
    const healthResponse = await fetch('http://localhost:8000/health');
    const healthData = await healthResponse.json();
    console.log('✅ Health check:', healthData);
    
    // Test modules endpoint
    const modulesResponse = await fetch('http://localhost:8000/modules');
    const modulesData = await modulesResponse.json();
    console.log('✅ Available modules:', Object.keys(modulesData.modules));
    
    // Test a sample query
    const queryResponse = await fetch('http://localhost:8000/query', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        query: "Hello, can you help me?",
        module: "acaps_compliance",
        agent: "acaps_reporter",
        custom_data: {}
      }),
    });
    
    const queryData = await queryResponse.json();
    console.log('✅ Sample query response:', queryData);
    
    console.log('\n🎉 All tests passed! Frontend should work correctly with the backend.');
    
  } catch (error) {
    console.error('❌ Connection test failed:', error.message);
    console.log('\nMake sure the backend server is running:');
    console.log('cd Backend && python run_server.py');
  }
};

testConnection();
