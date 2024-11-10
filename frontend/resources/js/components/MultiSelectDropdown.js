import React, { Component } from 'react';

class MultiSelectDropdown extends Component {
  constructor(props) {
    super(props);
    this.state = {
      selectedOptions: [],
      isDropdownOpen: false,
    };
  }

  toggleDropdown = () => {
    this.setState(prevState => ({ isDropdownOpen: !prevState.isDropdownOpen }));
  };

  handleOptionClick = (option) => {
    const { selectedOptions } = this.state;
    const { onSelectionChange } = this.props;
    let newSelectedOptions;
    if (selectedOptions.includes(option)) {
      newSelectedOptions = selectedOptions.filter(selected => selected !== option);
    } else {
      newSelectedOptions = [...selectedOptions, option];
    }

    this.setState({
      selectedOptions: newSelectedOptions,
    });

    // Call the callback function to update the parent state
    onSelectionChange(newSelectedOptions);
  };

  render() {
    const { choices } = this.props;
    const { labeltext } = this.props;
    const { selectedOptions, isDropdownOpen } = this.state;

    return (
      <div style={{ position: 'relative', width: '100%' }}>
        <div
          onClick={this.toggleDropdown}
          style={{
            border: '1px solid #ccc',
            padding: '8px',
            cursor: 'pointer',
            backgroundColor: '#fff',
            marginBottom: '4px',
       
          }}
        >
          {selectedOptions.length > 0
            ? selectedOptions.join(', ')
            :  labeltext }
          <span style={{ float: 'right' }}>
            {isDropdownOpen ? '▲' : '▼'}
          </span>
        </div>

        {isDropdownOpen && (
          <div
            style={{
              border: '1px solid #ccc',
              padding: '5px',
              position: 'absolute',
              backgroundColor: 'white',
              width: '100%',
              zIndex: 1000,
            }}
          >
            {choices.map(option => (
              <div
                key={option}
                onClick={() => this.handleOptionClick(option)}
                style={{
                  padding: '4px 8px',
                  cursor: 'pointer',
                  backgroundColor: selectedOptions.includes(option)
                    ? '#007BFF'
                    : '#fff',
                  color: selectedOptions.includes(option) ? '#fff' : '#000',
                  marginBottom: '2px',
                }}
              >
                {option}
              </div>
            ))}
          </div>
        )}

  
      </div>
    );
  }
}

export default MultiSelectDropdown;
