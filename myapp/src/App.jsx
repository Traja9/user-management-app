import { useState, useEffect } from 'react';
import './App.css';

export default function App() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [cursor, setCursor] = useState(null);
  const [hasMore, setHasMore] = useState(false);
  const [limit, setLimit] = useState(20);

  // Search states
  const [searchQuery, setSearchQuery] = useState('');
  const [suggestions, setSuggestions] = useState([]);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [selectedUser, setSelectedUser] = useState(null);
  const [searchLoading, setSearchLoading] = useState(false);

  // Fetch users from backend
  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async (nextCursor = null) => {
    try {
      setLoading(true);
      let url = `http://Savan9900990099.pythonanywhere.com/users?limit=${limit}`;
      
      if (nextCursor) {
        url += `&cursor=${nextCursor}`;
      }
      
      const response = await fetch(url);
      const data = await response.json();
      
      if (nextCursor) {
        setUsers([...users, ...data.users]);
      } else {
        setUsers(data.users);
      }
      
      setCursor(data.nextCursor);
      setHasMore(data.hasMore);
      setError(null);
    } catch (err) {
      setError('Failed to fetch users');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  // Smart search with autocomplete
  const handleSearchChange = async (value) => {
    setSearchQuery(value);
    
    if (value.length < 1) {
      setSuggestions([]);
      setShowSuggestions(false);
      return;
    }

    try {
      setSearchLoading(true);
      const response = await fetch(
        `http://Savan9900990099.pythonanywhere.com/search?q=${encodeURIComponent(value)}&limit=10`
      );
      const data = await response.json();
      setSuggestions(data.results);
      setShowSuggestions(true);
    } catch (err) {
      console.error('Search error:', err);
      setSuggestions([]);
    } finally {
      setSearchLoading(false);
    }
  };

  // Select suggestion and auto-fill
  const selectSuggestion = (user) => {
    setSearchQuery(user.name);
    setSelectedUser(user);
    setSuggestions([]);
    setShowSuggestions(false);
    setName(user.name);
    setEmail(user.email);
  };

  const addUser = async (e) => {
    e.preventDefault();
    
    if (!name || !email) {
      alert('Please fill in all fields');
      return;
    }

    try {
      const response = await fetch('https://Savan9900990099.pythonanywhere.com/users', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name, email })
      });

      if (response.ok) {
        setName('');
        setEmail('');
        setSearchQuery('');
        setSelectedUser(null);
        fetchUsers();
        alert('User added successfully!');
      } else {
        alert('Failed to add user');
      }
    } catch (err) {
      alert('Error adding user');
      console.error(err);
    }
  };

  const loadMore = () => {
    if (cursor && hasMore) {
      fetchUsers(cursor);
    }
  };

  return (
    <div className="container">
      <h1>User Management App</h1>

      <div className="form-section">
        <h2>Search & Add User</h2>
        
        <div className="search-container">
          <input
            type="text"
            placeholder="Search by name (e.g., Amanda, John...)"
            value={searchQuery}
            onChange={(e) => handleSearchChange(e.target.value)}
            className="search-input"
          />
          
          {searchLoading && <p className="search-status">Searching...</p>}
          
          {showSuggestions && suggestions.length > 0 && (
            <div className="suggestions-dropdown">
              {suggestions.map((user) => (
                <div
                  key={user.id}
                  className="suggestion-item"
                  onClick={() => selectSuggestion(user)}
                >
                  <div className="suggestion-name">{user.name}</div>
                  <div className="suggestion-email">{user.email}</div>
                </div>
              ))}
            </div>
          )}
          
          {showSuggestions && suggestions.length === 0 && searchQuery.length > 0 && !searchLoading && (
            <div className="suggestions-dropdown">
              <div className="suggestion-item no-results">No users found</div>
            </div>
          )}
        </div>

        {selectedUser && (
          <div className="selected-user-info">
            <p><strong>Selected:</strong> {selectedUser.name}</p>
            <p><strong>Email:</strong> {selectedUser.email}</p>
            <p><strong>ID:</strong> {selectedUser.id}</p>
          </div>
        )}

        <form onSubmit={addUser} className="add-user-form">
          <input
            type="text"
            placeholder="Name"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <button type="submit">Add User</button>
        </form>
      </div>

      <div className="users-section">
        <h2>Users List ({users.length} loaded)</h2>
        
        {error && <p style={{ color: 'red' }}>{error}</p>}
        
        {users.length > 0 ? (
          <>
            <table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Name</th>
                  <th>Email</th>
                </tr>
              </thead>
              <tbody>
                {users.map((user) => (
                  <tr key={user.id}>
                    <td>{user.id}</td>
                    <td>{user.name}</td>
                    <td>{user.email}</td>
                  </tr>
                ))}
              </tbody>
            </table>
            
            {hasMore && (
              <button 
                onClick={loadMore} 
                disabled={loading}
                className="load-more-btn"
              >
                {loading ? 'Loading...' : 'Load More'}
              </button>
            )}
            {!hasMore && users.length > 0 && (
              <p className="end-message">No more users to load</p>
            )}
          </>
        ) : (
          !loading && <p>No users found</p>
        )}
      </div>
    </div>
  );
}
